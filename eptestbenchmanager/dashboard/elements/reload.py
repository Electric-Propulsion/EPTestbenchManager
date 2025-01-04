from ..dashboardelement import DashboardElement
from flask_socketio import emit, Namespace, SocketIO
from flask import render_template

class Reload(DashboardElement):
    def __init__(self, uid: str, socketio: SocketIO = None):
        super().__init__(uid, socketio)
        self.namespace = f"/{uid}"
        self.socketio.on_namespace(Namespace(self.namespace))
    
    def render_html(self):
        return ""
    
    def render_js(self):
        data = {
            "namespace": self.namespace,
            "uid": self.uid
        }
        return render_template("elements/reload.js", data=data)
    
    def reload(self):
        self.socketio.emit("reload", namespace=self.namespace)