from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit, Namespace
from threading import Thread
import os
from pathlib import Path

from .pages import MainPage, InstrumentDetail
from .elements import ExperimentControl

class DashboardManager:
     def __init__(self, testbench_manager: "TestbenchManager"):
          self.testbench_manager = testbench_manager
          self.app = Flask('eptestbenchmanager', static_folder='dashboard/assets/static', template_folder='dashboard/assets/templates')
          self.socketio = SocketIO(self.app)
          self.app.config["SECRET_KEY"] = 'testkey!' #TODO: change me!

     
     def configure(self):
          # Main page route
          @self.app.route('/')
          def index():
               page = self.create_page(MainPage, [self.testbench_manager])
               return page.render()
          
          # Instrument detail page routes
          vints =  self.testbench_manager.connection_manager._virtual_instruments.values()
          for vint in vints:
               def make_instrument_detail(vint):
                    @self.app.route(f'/instrument/{vint.uid}', endpoint=f'instrument_detail_{vint.uid}')
                    def instrument_detail():
                         return vint._detail_page.render()
               make_instrument_detail(vint)

          
          # Special routes for downloading files
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
     
     def create_page(self, page_class: 'DashboardPage', args):
          page_object = page_class(*args, **{'socketio': self.socketio, 'app': self.app})
          return page_object


     def run(self):
          print("Starting dashboard - this will block the main thread")
          self.socketio.run(self.app)