from . import DashboardElement

class InstrumentElement(DashboardElement):
    
    def __init__(self, uid: str, title: str, testbench_manager: "TestbenchManager", instrument: "VirtualInstrument"):
        super().__init__(uid, title, testbench_manager)
        self._instrument = instrument