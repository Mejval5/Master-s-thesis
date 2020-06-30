
from lib.HelperMethods import *

from lib.Loop import Loop
from lib.InitializeWindow import InitializeWindow
from lib.Display import Display
from lib.GuiSetup import GuiSetup
from lib.Config import Config
from lib.Rotation import Rotation
from lib.Angle import Angle

class MainController():

	def __init__(self):
		self.config = Config()
		self.angle = Angle(self)
		self.rotationObject = Rotation(self)

		self.mainWindow = InitializeWindow(self).get_window()

		self.display = Display(self)
		self.guiElements = GuiSetup(self)

		self.loop = Loop(self)

MainController()