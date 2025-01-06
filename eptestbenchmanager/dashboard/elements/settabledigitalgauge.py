from flask import render_template
from . import DigitalGauge

class SettableDigitalGauge(DigitalGauge):

    def __init__(self, uid: str, name: str, unit: str, link: str, virtual_instrument: "VirtualInstrument", socketio=None):
        super().__init__(uid, name, unit, link, socketio)
        self.virtual_instrument = virtual_instrument
        self.configure()

    def render_html(self):
        data = {
            "uid": self.uid,
            "name": self.name,
            "unit": self.unit,
            "link": self.link,
        }
        return render_template("elements/settable_digital_gauge.html", data=data)
    
    def render_js(self):
        data = {"namespace": self.namespace, "uid": self.uid}
        return render_template("elements/settable_digital_gauge.js", data=data)
    
    def configure(self):
        @self.socketio.on("set_value", namespace=self.namespace)
        def receive_value(data):
            try:
                value = float(data["value"]) #assume it's a number
            except ValueError:
                value = data["value"]
            self.virtual_instrument.set_value(value)
