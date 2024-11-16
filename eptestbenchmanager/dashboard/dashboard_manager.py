from dash import Dash, dcc, html, Input, Output, callback
from threading import Thread
import os


class DashboardManager:

    def __init__(self, testbench_manager: "TestbenchManager"):
        self.views: dict = {}
        self._testbench_manager = testbench_manager
        self._app = Dash(
            "Dashboard",
            suppress_callback_exceptions=True,
            update_title=None,
            assets_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets'),
            title="EPDashboard",
        )
        self._app.layout = html.Div(
            [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
        )
        self._app_thread: Thread = None

        self.register_callbacks(self._app)

    def configure(self) -> None:
        pass

    def add_view(self, view: "DashboardView") -> None:
        self.views[view.uid] = view
        print(f"added view {view.uid}")

    def remove_view(self, view: "DashboardView") -> None:
        self.views.pop(view.uid)

    def _run_app(self) -> None:
        self._app.run_server(debug=True, use_reloader=False, host="0.0.0.0")

    def run(self) -> None:
        self._client_thread = Thread(
            target=self._run_app, name="Dashboard App- Thread", daemon=True
        )
        self._client_thread.start()

    def register_callbacks(self, app):
        @app.callback(Output("page-content", "children"), Input("url", "pathname"))
        def display_page(pathname):
            page_name = pathname[1:]
            print(f"accessing page {page_name}")
            print(f"views: {self.views}")
            if page_name == "":
                page_name = "home"
            if page_name not in self.views:
                return "404"
            return self.views[page_name].div
