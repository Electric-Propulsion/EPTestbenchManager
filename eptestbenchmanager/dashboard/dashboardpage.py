from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from flask import Flask
from flask_socketio import SocketIO

if TYPE_CHECKING:
    from eptestbenchmanager.dashboard import DashboardElement


class DashboardPage(ABC):
    """Abstract base class for a dashboard page.

    Attributes:
        app (Flask): The Flask application instance.
        socketio (SocketIO): The Flask-SocketIO instance.
        route (str): The route for the dashboard page.
    """

    def __init__(self, app: Flask, socketio: SocketIO, route: str):
        """Initializes the DashboardPage with the given app, socketio, and route.

        Args:
            app (Flask): The Flask application instance.
            socketio (SocketIO): The Flask-SocketIO instance.
            route (str): The route for the dashboard page.
        """
        self.app = app
        self.socketio = socketio
        self.route = route

    def configure(self):
        """Configures the route for the dashboard page."""

        @self.app.route(self.route)
        def page_content(self):
            return self.render()

    @abstractmethod
    def render(self):
        """Renders the content of the dashboard page.

        Returns:
            str: The HTML content of the page.

        Raises:
            NotImplementedError: If the method is not implemented, which must be done by subclasses.
        """
        return NotImplementedError("Implement Page content")

    def render_components_html(self, components: list["DashboardElement"]):
        """Renders the HTML for the given components.

        Args:
            components (list[DashboardElement]): The list of dashboard elements.

        Returns:
            str: The concatenated HTML of all components.
        """
        return "".join([component.render_html() for component in components])

    def render_components_js(self, components: list["DashboardElement"]):
        """Renders the JavaScript for the given components.

        Args:
            components (list[DashboardElement]): The list of dashboard elements.

        Returns:
            str: The concatenated JavaScript of all components.
        """
        return "".join([component.render_js() for component in components])
