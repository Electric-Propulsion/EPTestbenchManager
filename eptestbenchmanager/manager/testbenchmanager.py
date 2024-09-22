from eptestbenchmanager.connections import ConnectionManager
from eptestbenchmanager.monitor import TestbenchMonitor


class TestbenchManager:

    def __init__(self):
        self.monitor = TestbenchMonitor()
        self.connection_manager = ConnectionManager()
        self.alert_manager = AlertManager()
        self.communication_engine = CommunicationEngine()
        self.chat_manager = ChatManager()
        self.dashboard_manager = DashboardManager()
        self.runner = ExperimentRunner()

    def start(self):
        pass
        # TODO
