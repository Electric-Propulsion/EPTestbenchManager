from flask import Flask, render_template
from flask_socketio import SocketIO, emit, Namespace
from threading import Thread

class DashboardManager:
     def __init__(self, testbench_manager: "TestbenchManager"):
          self.testbench_manager = testbench_manager
          self.app = Flask('eptestbenchmanager')
          self.socketio = SocketIO(self.app)
          self.app.config["SECRET_KEY"] = 'testkey!' #TODO: change me!

     
     def configure(self):
          # Set up all the pages, i.e. the routes
          @self.app.route('/')
          def index():
               return f"Hello, World!"



     def run(self):
          print("Starting dashboard - this will block the main thread")
          self.socketio.run(self.app)