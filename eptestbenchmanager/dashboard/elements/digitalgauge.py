from . import CurrentValueElement

class DigitalGauge(CurrentValueElement):
    def render_html(self):
        return f"""
        <div id="{self.uid}" class="digital-gauge">
            <h2>{self.name}</h2>
            <h1 class="value"></h1>
            <p class="unit"></p>
        </div>
        """
    
    def render_js(self):
        return f"""
        var {self.uid}_socket = io('{self.namespace}');
        {self.uid}_socket.on('update', function(data) {{
            document.getElementById('{self.uid}').getElementsByClassName('value')[0].innerText = data.value;
            document.getElementById('{self.uid}').getElementsByClassName('unit')[0].innerText = data.unit;
        }});
        """
