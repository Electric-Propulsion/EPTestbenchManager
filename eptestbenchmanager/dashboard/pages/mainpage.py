from ..dashboardpage import DashboardPage

class MainPage(DashboardPage):
    def __init__(self, app, socketio, testbench_manager):
        super().__init__(app, socketio, "/")
        vints =  testbench_manager.connection_manager._virtual_instruments.values()
        self.components = [vint._gauge for vint in vints]
        self.experiment_control = testbench_manager.dashboard.experiment_control
    def render(self):
        return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Dashboard</title>
                <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
                <link rel="stylesheet" href="/static/style.css">
                <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.1/socket.io.min.js"></script>
            </head>
            <body>
                <h1>Dashboard</h1>
                <div id="experiment_control_segment">
                    {self.experiment_control.render_html()}
                </div>
                <script>
                    {self.experiment_control.render_js()}
                </script>
                <div id="dashboard">
                    {self.render_components_html(self.components)}
                </div>
                <script>
                    {self.render_components_js(self.components)}
                </script>
            </body>
        </html>
        """