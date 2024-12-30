from ..dashboardpage import DashboardPage

class MainPage(DashboardPage):
    def __init__(self, app, socketio, testbench_manager):
        super().__init__(app, socketio, "/")
        vints =  testbench_manager.connection_manager._virtual_instruments.values()
        self.components = [vint._gauge for vint in vints]
    def render(self):
        return f"""
        <html>
            <head>
                <title>Dashboard</title>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.1/socket.io.min.js"></script>
            </head>
            <body>
                <h1>Dashboard</h1>

                <div id="dashboard">
                    {self.render_components_html(self.components)}
                </div>
                <script>
                    {self.render_components_js(self.components)}
                </script>

                <div id="experiment-control">
                    <h1>Experiment Control</h1>
                    <button id="start-experiment">Start Experiment</button>
                    <button id="abort-experiment">Abort Experiment</button>
                </div>
            </body>
        </html>
        """