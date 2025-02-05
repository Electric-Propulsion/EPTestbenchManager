from .. import DashboardPage
from ..elements import Editor


class ConfigEditor(DashboardPage):

    def __init__(
        self,
        testbench_manager,
        config_dir,
        config_file,
        app=None,
        socketio=None,
    ):
        super().__init__(app, socketio, None)

        self.editor = Editor(
            f"{config_file.replace('.','_')}_editor",
            testbench_manager,
            config_dir,
            config_file,
            self.socketio,
        )

    def render(self):
        return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Editing {self.editor.filename}</title>
                <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
                <link rel="stylesheet" href="/static/style.css">
                <script src="/static/socket.io.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js"></script>
            </head>
            <body>
                <a href="/" class="home_link">‹</a>
                <div id="editor_segment">
                    {self.editor.render_html()}
                </div>
                <script>
                    {self.editor.render_js()}
                </script>
            </body>
            """
