from abc import ABC, abstractmethod
from flask import Flask
from flask_socketio import SocketIO
from . import DashboardElement

class DashboardPage(ABC):
    def __init__(self, app: Flask, socketio: SocketIO, route: str):
        self.app = app
        self.socketio = socketio
        self.route = route


    def configure(self):
        @self.app.route(self.route)
        def page_content(self):
            return self.render()
        
    @abstractmethod
    def render(self):
        return NotImplementedError("Implement Page content")
    
    def render_components_html(self, components: list[DashboardElement]):
        return "".join([component.render_html() for component in components])
    
    def render_components_js(self, components: list[DashboardElement]):
        return "".join([component.render_js() for component in components])
    
