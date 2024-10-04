from . import DashboardView
from .elements import Gauge


@staticmethod
def get_home_view(testbench_manager: "TestbenchManager") -> DashboardView:
    view = DashboardView("home", "Home", testbench_manager)
    view.add_element(Gauge("gauge1", "Gauge 1", testbench_manager))
    view.register_callbacks()
    return view
