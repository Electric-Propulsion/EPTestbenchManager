from abc import ABC, abstractmethod
from flask_socketio import SocketIO

class DashboardElement(ABC):
    def __init__(self, uid: str, socketio: SocketIO = None):
        self.uid = uid
        self.socketio = socketio

    @abstractmethod
    def render_html(self):
        return NotImplementedError("Implement render method")
    
    @abstractmethod
    def render_js(self):
        return NotImplementedError("Implement render method")
    
    