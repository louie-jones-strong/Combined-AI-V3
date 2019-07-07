import time
import Shared.OutputFormating as Formating
from Shared.OSCalls import ClearShell

class LoadingBar():

	def __init__(self, allowUpdate=True):
		self.CurrentProgress = 0
		self.CurrentText = None
		self.Resolution = 100
		self.LastUpdateTime = 0
		self.AllowUpdate = allowUpdate
		return

	def Update(self, progress, text=None, numDone=None, totalNum=None):
		progress = max(progress, 0)
		progress = min(progress, 1)

		progress = int(progress*self.Resolution)

		if time.time()-self.LastUpdateTime >= 0.15 or progress == self.Resolution:

			if progress != self.CurrentProgress or text != self.CurrentText:
				ClearShell()
				bar = "#"*progress
				fill = " "*(self.Resolution-progress)
				print("|"+bar+fill+"|")
				self.CurrentProgress = progress

				if text != None:
					print(text)
					self.CurrentText = text
				
				if numDone != None and totalNum != None:
					output = Formating.SplitNumber(numDone)
					output += "/"
					output += Formating.SplitNumber(totalNum)
					output += " "+str(round(progress, 2))+"%"

					print(output)

				self.LastUpdateTime = time.time()
		return
