from . import VirtualInstrument

class ExperimentStatusVirtualInstrument(VirtualInstrument):
    def command(self, command):
        raise NotImplementedError("ExperimentStatusVirtualInstrument does not support commands")