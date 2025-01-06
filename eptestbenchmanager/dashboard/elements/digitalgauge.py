from flask import render_template
from . import CurrentValueElement


class DigitalGauge(CurrentValueElement):
    """A class to represent a digital gauge element in the dashboard.

    Inherits from CurrentValueElement.

    Attributes:
        uid (str): Unique identifier for the gauge.
        name (str): Name of the gauge.
        unit (str): Unit of measurement for the gauge.
        link (str): Link associated with the gauge.
        namespace (str): Namespace for the gauge.
    """

    def render_html(self):
        """Renders the HTML for the digital gauge.

        Returns:
            str: Rendered HTML template for the digital gauge.
        """
        data = {
            "uid": self.uid,
            "name": self.name,
            "unit": self.unit,
            "link": self.link,
        }
        return render_template("elements/digital_gauge.html", data=data)

    def render_js(self):
        """Renders the JavaScript for the digital gauge.

        Returns:
            str: Rendered JavaScript template for the digital gauge.
        """
        data = {"namespace": self.namespace, "uid": self.uid}
        return render_template("elements/digital_gauge.js", data=data)
