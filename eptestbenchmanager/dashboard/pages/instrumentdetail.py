from ..dashboardpage import DashboardPage
from ..elements import Reload

class InstrumentDetail(DashboardPage):

    def __init__(self, virtual_instrument, testbench_manager, app = None, socketio = None):
        super().__init__(app, socketio,f'/instrument/{virtual_instrument.uid}')
        self.testbench_manager = testbench_manager
        self.virtual_instrument = virtual_instrument
        self.instrument_name = virtual_instrument.name
        self.graphs = []
        self.rolling_graph = virtual_instrument._rolling_storage.graph
        self.reload = Reload('reload', self.socketio)
        self.gauge = virtual_instrument._gauge
        self.update_graphs()

    
    def render(self):
        return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Instrument Detail</title>
                <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
                <link rel="stylesheet" href="/static/style.css">
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.1/socket.io.min.js"></script>
            </head>
            <body>
                <a href="/" class="home_link">‹</a>
                <h1>{self.instrument_name} Detail</h1>
                <div id="gauge_segment" style="display: flex; justify-content: center;">
                    {self.gauge.render_html()}
                </div>
                <script>
                    {self.gauge.render_js()}
                </script>
                <div id="rolling_graph_segment">
                    {self.rolling_graph.render_html()}
                </div>
                <script>
                    {self.rolling_graph.render_js()}
                </script>

                <div id="recording_graphs_segment">
                    {self.render_components_html(self.graphs)}
                </div>
                <script>
                    {self.render_components_js(self.graphs)}
                </script>
                <script>
                    {self.reload.render_js()}
                </script>
            </body>
        </html>
        """
    
    def update_graphs(self):
        old_graphs = self.graphs
        self.graphs = [recording.graph for recording in self.virtual_instrument._recordings.values()]

        self.reload.reload()

        for graph in self.graphs:
            if graph not in old_graphs:
                graph.update()
        