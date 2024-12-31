from flask import render_template
from . import CurrentValueElement

class DigitalGauge(CurrentValueElement):
    def render_html(self):
        data = {
            "uid": self.uid,
            "name": self.name,
            "unit": self.unit,
        }
        return render_template("elements/digital_gauge.html", data=data)
    
    def render_js(self):
        data = {
            "namespace": self.namespace,
            "uid": self.uid
        }
        return render_template("elements/digital_gauge.js", data=data)
