import random
from . import DashboardView


@staticmethod
def get_home_view(testbench_manager: "TestbenchManager") -> DashboardView:
    view = DashboardView(
        "home",
        "Home",
        testbench_manager,
    )
    # temporary!
    # #for element in testbench_manager.connection_manager.virtual_instruments["gaussian_noise_1"].dashboard_elements.values():
    #     view.add_element(element)
    # view.register_callbacks()
    return view
