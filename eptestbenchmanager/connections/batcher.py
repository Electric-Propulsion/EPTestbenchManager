from threading import Thread
from time import monotonic, sleep


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
        self._vints = {} #key is batching argument value

        self._polling_interval = polling_interval

        self._polling_thread = Thread(
            target=self._polling_loop,
            name="A Batching Thread",
            daemon=True,
        )

    def add_polling_instrument(self, instrument, batching_argument_value):
        self._vints[batching_argument_value] = instrument

    def _polling_loop(self):
        getter_arguments = self._getter_arguments | self._get_mux_arguments(self._batching_scheme)
        getter_function = (
            (
                lambda: getattr(self._physical_instrument, self._getter_function)(
                    **getter_arguments
                )
            )
        )

        while True:
            print("batcher running!")
            next_poll_time = monotonic() + self._polling_interval / 1000
            try:
                values = getter_function()
                values_by_argument = self._get_demux_function(self._batching_scheme)(values)
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
        self._polling_thread.start()


    # we have to assume that no new instruments were added between calls to get_mux_args and get_demux_function

    def _get_mux_arguments(self, batching_scheme: str) -> dict:
        match batching_scheme:
            case "SCPI_chanlist":
                return {
                    "channel": list(self._vints.keys())
                }  # expected to be a list

    def _get_demux_function(self, batching_scheme: str) -> callable:
        match batching_scheme:
            case "SCPI_chanlist":
                def demux_function(values):
                    if(len(values) != len(self._vints.keys())):
                        raise ValueError("Cannot demux; wrong number of values returned")
                    ret = {list(self._vints.keys())[i]: values[i] for i in range(len(values))}   
                    print(ret)
                    return ret
                return demux_function
