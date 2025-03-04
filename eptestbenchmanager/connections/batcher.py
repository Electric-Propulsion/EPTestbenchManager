import logging
from threading import Thread, Event
from time import monotonic, sleep

logger = logging.getLogger(__name__)


class Batcher:
    def __init__(
        self,
        physical_instrument,
        getter_function: callable,
        getter_arguments: dict,
        batching_scheme: str,
        polling_interval: int,
    ):

        self._physical_instrument = physical_instrument
        self._getter_function = getter_function
        self._getter_arguments = getter_arguments
        self._batching_scheme = batching_scheme
        self._vints = {}  # key is batching argument value

        self._polling_interval = polling_interval

        self._polling_thread = Thread(
            target=self._polling_loop,
            name="A Batching Thread",
            daemon=True,
        )
        self._stop_event = Event()

    def add_polling_instrument(self, instrument, batching_argument_value):
        self._vints[batching_argument_value] = instrument

    def _polling_loop(self):
        getter_arguments = self._getter_arguments | self._get_mux_arguments(
            self._batching_scheme
        )
        getter_function = lambda: getattr(
            self._physical_instrument, self._getter_function
        )(**getter_arguments)

        while True:
            next_poll_time = monotonic() + self._polling_interval / 1000
            if self._stop_event.is_set():
                return  # Exit the thread
            try:
                values = getter_function()
                values_by_argument = self._get_demux_function(self._batching_scheme)(
                    values
                )
                for arg, value in values_by_argument.items():
                    self._vints[arg].set_value(value)

            except Exception as e:
                print(f"A batcher encountered exception: {e}")
            sleep_time = next_poll_time - monotonic()
            if sleep_time > 0:
                sleep(sleep_time)
            else:
                # We missed the polling interval
                print(
                    f"EPTestbenchManager: A batcher missed a polling interval by {-sleep_time} seconds"
                )
                pass

    def start_poll(self) -> None:
        """Starts the polling thread."""
        self._stop_event.clear()
        try:
            self._polling_thread.start()
        except RuntimeError:
            logger.error(f"Instrument {self.name} polling thread already started.")

    def halt_poll(self) -> None:
        """Stops the polling thread."""
        self._stop_event.set()

    def join_poll(self) -> None:
        """Joins the polling thread."""
        if self._polling_thread.is_alive():
            self._polling_thread.join()

    # we have to assume that no new instruments were added between calls to get_mux_args and get_demux_function

    def _get_mux_arguments(self, batching_scheme: str) -> dict:
        match batching_scheme:
            case "SCPI_chanlist":
                return {"channel": list(self._vints.keys())}  # expected to be a list
            case "custom_USBTC08":
                return {}


    def _get_demux_function(self, batching_scheme: str) -> callable:
        match batching_scheme:
            case "SCPI_chanlist":

                def demux_function(values):
                    if isinstance(values, list):
                        # we've presumably got more than one value back
                        if len(values) != len(self._vints.keys()):
                            raise ValueError(
                                "Cannot demux; wrong number of values returned"
                            )
                        return {
                            list(self._vints.keys())[i]: values[i]
                            for i in range(len(values))
                        }
                    else:
                        # we've only got a single reading back, not as a list
                        if len(self._vints.keys()) != 1:
                            raise ValueError(
                                "Cannot demux; expected multiple values but only got one"
                            )
                        return {
                            list(self._vints.keys())[0]: values
                        }  # 'values' is actually just a single number

                return demux_function
            case "custom_USBTC08":
                def demux_function(values):
                    # values is a list of eight temperatures corrisponding to channels 1-8
                    return {
                        list(self._vints.keys())[i]: values[list(self._vints.keys())[i]] for i in range(len(self._vints))
                    }
                return demux_function
