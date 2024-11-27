from dash import dcc, html
from typing import Any


class DashboardView:
    def __init__(self, uid: str, title: str, testbench_manager: "TestbenchManager"):
        self.uid = uid
        self.title = title
        self._testbench_manager = testbench_manager
        self._dashboard_manager = testbench_manager.dashboard_manager
        self._elements = {}

    def add_element(self, element: "DashboardElement") -> None:
        self._elements[element.uid] = element
        self._elements[element.uid].register_callbacks()

    def remove_element(self, element: "DashboardElement") -> None:
        self._elements.pop(element.uid)

    def get_element(self, uid: str) -> "DashboardElement":
        return self._elements[uid]

    @property
    def div(self) -> Any:  # TODO
        return html.Div(
            [
                # View divs
                html.H1(self.title),
                html.P(f"uid: {self.uid}"),
                dcc.Link("Home", href="/", className="nav-menu-item"),
                # Element divs
                html.Div([element.div for element in self._elements.values()]),
            ]
        )

    def register_callbacks(self) -> None:
        pass
        # for element in self._elements.values():
        #     element.register_callbacks()
