from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit, Namespace
from threading import Thread
import os
from pathlib import Path

from .pages import MainPage
from .elements import ExperimentControl

class DashboardManager:
     def __init__(self, testbench_manager: "TestbenchManager"):
          self.testbench_manager = testbench_manager
          self.app = Flask('eptestbenchmanager', static_folder='dashboard/assets/static', template_folder='dashboard/assets/templates')
          self.socketio = SocketIO(self.app)
          self.app.config["SECRET_KEY"] = 'testkey!' #TODO: change me!

     
     def configure(self):
          # Set up all the pages, i.e. the routes
          @self.app.route('/')
          def index():
               page = MainPage(self.app, self.socketio, self.testbench_manager)
               return page.render()
          
          @self.app.route('/archive/<archive>')
          def download_archive(archive):
               archive_dir = os.path.join(Path(os.path.abspath(__package__)).parent, "eptestbenchmanager", "logs", "archives") # what a terrific line of code.
               print(f"downloading archive {archive}")
               try:
                    return send_from_directory(archive_dir, f"{archive}")
               except Exception as e:
                    print(f"Error starting experiment: {e}")
          
          # set up the experiment control elements
          self.experiment_control = self.create_element(ExperimentControl, args=['experiment_control', self.testbench_manager])

     def create_element(self, element_class: 'DashboardElement', args):
          print(args)
          element_object = element_class(*args, **{'socketio': self.socketio})
          return element_object


     def run(self):
          print("Starting dashboard - this will block the main thread")
          self.socketio.run(self.app)