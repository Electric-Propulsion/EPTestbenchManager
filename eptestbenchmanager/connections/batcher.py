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
        self._batching_argument_values = []

        self._values = {}

        self._polling_interval = polling_interval

        self._polling_thread = Thread(
            target=self._polling_loop,
            name=f"{self._physical_instrument.name} Batching Thread",
            daemon=True,
        )

    def _polling_loop(self):
        while True:
            next_poll_time = monotonic() + self._polling_interval / 1000
            try:
                value = self._getter_function()
                self._set_value(value)
            except Exception as e:
                print(f"Instrument {self.name} encountered exception: {e}")
            sleep_time = next_poll_time - monotonic()
            if sleep_time > 0:
                sleep(sleep_time)
            else:
                # We missed the polling interval
                print(
                    f"EPTestbenchManager: A batcher for {self._physical_instrument.name} missed a polling interval by {-sleep_time} seconds"
                )
                pass

    def start_poll(self) -> None:
        """Starts the polling thread."""
        self._polling_thread.start()

    def _get_mux_arguments(self, batching_scheme: str) -> dict:
        match batching_scheme:
            case "SCPI_chanlist":
                return {
                    "channels": self._batching_argument_values
                }  # expected to be a list

    def _get_demux_function(self, batching_scheme: str) -> callable:
        match batching_scheme:
            case "SCPI_chanlist":
                return lambda value: value
