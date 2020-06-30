
from lib.HelperMethods import *

from lib.Loop import Loop
from lib.InitializeWindow import InitializeWindow
from lib.GuiSetup import GuiSetup
from lib.Config import Config

class MainController():

	def __init__(self):
		self.config = Config()

		self.mainWindow = InitializeWindow(self).get_window()

		self.guiElements = GuiSetup(self)

		self.loop = Loop(self)

MainController()