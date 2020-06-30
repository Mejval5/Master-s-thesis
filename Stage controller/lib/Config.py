class Config():

	def __init__(self):
		# Default monitor to be used as display
		self.monitor=1	
	
		self.name = "Beam controller"
		self.outputX=800
		self.outputY=600
		self.previewX=640
		self.previewY=480
		self.correctionFactor=196

		self.centerX=0.5
		self.centerY=0.5

		self.angle=0
		self.angleTime=0

		self.timeStamp=0
		# Timeframe in which the program will scan for display adapters
		self.waitForDisplays=0.1
		# 1 = start with display on
		self.startDisplay = 0
		# 1 = start with mouse changing center
		self.startChangeCenter=0
		self.active = True