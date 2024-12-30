from ..dashboardelement import DashboardElement
from abc import ABC, abstractmethod
from flask_socketio import emit, Namespace

class CurrentValueElement(DashboardElement, ABC):
    class CurrentValueNamespace(Namespace):
        def on_connect(self):
            print("Client connected to CurrentValueNamespace")
            emit('update', {'value': self.element.value, 'unit': self.element.unit}, namespace=self.element.namespace)

        def __init__(self, namespace, element):
            super().__init__(namespace)
            self.element = element

    def __init__(self, uid: str, name: str):
        super(DashboardElement, self).__init__(uid)
        self.name = name
        self.value = None
        self.unit = None

        self.namespace = f"/{uid}"
        self.socketio.on_namespace(self.CurrentValueNamespace(self.namespace, self))

        

    def set_value(self, value, unit):
        self.value = value
        self.unit = unit

        # Derived classes must have client-side JS that listens for the 'update' event
        emit('update', {'value': self.value, 'unit': self.unit}, namespace=self.namespace)

    




    