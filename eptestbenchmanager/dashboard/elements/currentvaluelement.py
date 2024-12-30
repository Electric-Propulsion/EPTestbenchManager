from ..dashboardelement import DashboardElement
from flask_socketio import emit, Namespace, SocketIO

class CurrentValueElement(DashboardElement):
    class CurrentValueNamespace(Namespace):
        def on_connect(self):
            print("Client connected to CurrentValueNamespace")
            emit('update', {'value': self.element.value, 'unit': self.element.unit}, namespace=self.element.namespace)

        def __init__(self, namespace, element):
            super().__init__(namespace)
            self.element = element

    def __init__(self, uid: str, name: str, unit: str = None, socketio: SocketIO = None,):
        super().__init__(uid, socketio)
        self.name = name
        self.value = None
        self.unit = unit

        self.namespace = f"/{uid}"
        self.socketio.on_namespace(self.CurrentValueNamespace(self.namespace, self))

        

    def set_value(self, value):
        self.value = value

        # Derived classes must have client-side JS that listens for the 'update' event
        self.socketio.emit('update', {'value': self.value, 'unit': self.unit}, namespace=self.namespace)

    




    