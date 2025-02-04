from ..dashboardpage import DashboardPage
from ..elements import Reload


class MainPage(DashboardPage):
    """MainPage class for the dashboard.

    This class represents the main page of the dashboard, inheriting from DashboardPage. It
    initializes the components, experiment control, and archive download elements, and provides a
    method to render the HTML and JavaScript for the page.

    Attributes:
        components (list): List of gauge components from virtual instruments.
        experiment_control (ExperimentControl): The experiment control element.
        archive_download (ArchiveDownload): The archive download element.
    """

    def __init__(self, testbench_manager, app, socketio):
        """Initializes the MainPage with the given parameters.

        Args:
            testbench_manager (TestbenchManager): The testbench manager instance.
            app (Flask): The Flask application instance.
            socketio (SocketIO): The SocketIO instance.
        """
        super().__init__(app, socketio, "/")
        vints = testbench_manager.connection_manager.virtual_instruments.values()
        self.components = [vint.gauge for vint in vints]
        self.experiment_control = testbench_manager.dashboard.experiment_control
        self.archive_download = testbench_manager.report_manager.ui_element
        self.apparatus_control = testbench_manager.connection_manager.ui_element
        self.reload = Reload("reload", self.socketio)
        testbench_manager.connection_manager.register_reload(self.reload)

    def render(self):
        """Renders the HTML and JavaScript for the main page.

        Returns:
            str: The HTML and JavaScript content for the main page.
        """
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
                <div id="apparatus_control_segment">
                    {self.apparatus_control.render_html()}
                </div>
                <script>
                    {self.apparatus_control.render_js()}
                </script>
                <div id="experiment_control_segment">
                    {self.experiment_control.render_html()}
                </div>
                <script>
                    {self.experiment_control.render_js()}
                </script>
                <div id="archive_download_segment">
                    {self.archive_download.render_html()}
                </div>
                <script>
                    {self.archive_download.render_js()}
                </script>

                <div id="dashboard">
                    {self.render_components_html(self.components)}
                </div>
                <script>
                    {self.render_components_js(self.components)}
                </script>
                 <script>
                    {self.reload.render_js()}
                </script>
            </body>
        </html>
        """
