from dash import Dash, dcc, html, Input, Output, callback

class DashboardManager:

    def __init__(self, testbench_manager: "TestbenchManager"):
        self.views: dict = {}
        self._testbench_manager = testbench_manager
        self._app = Dash('Dashboard')
        self._app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ])

        self.callbacks(self._app)

    def configure(self) -> None:
        pass

    def add_view(self, view: "DashboardView") -> None:
        self.views[view.uid] = view

    def remove_view(self, view: "DashboardView") -> None:
        self.views.pop(view.uid)

    def run(self) -> None:
        self._app.run(debug=True)

    def callbacks(self, app):
        @app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
        def display_page(pathname):
            page_name = pathname[1:]
            print(f"accessing page {page_name}")
            return self.views[page_name].layout
