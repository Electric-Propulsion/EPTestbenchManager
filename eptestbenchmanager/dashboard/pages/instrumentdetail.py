from ..dashboardpage import DashboardPage

class InstrumentDetail(DashboardPage):

    def __init__(self, virtual_instrument, testbench_manager, app = None, socketio = None):
        super().__init__(app, socketio,f'/instrument/{virtual_instrument.uid}')
        self.testbench_manager = testbench_manager
        self.virtual_instrument = virtual_instrument
        self.graphs = []
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
                <h1>Instrument Detail</h1>
                <div id="graph_segment">
                    {self.render_components_html(self.graphs)}
                </div>
                <script>
                    {self.render_components_js(self.graphs)}
                </script>
            </body>
        </html>
        """
    
    def update_graphs(self):
        old_graphs = self.graphs
        self.graphs = [recording.graph for recording in self.virtual_instrument._recordings]

        for graph in self.graphs:
            if graph not in old_graphs:
                graph.update()
        