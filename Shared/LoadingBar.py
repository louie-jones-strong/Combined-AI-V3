import time
import Shared.OutputFormating as Formating

class LoadingBar():

	def __init__(self, logger):
		self.Logger = logger
		self.CurrentProgress = 0
		self.CurrentText = None
		self.Resolution = 100
		self.LastUpdateTime = 0
		return

	def Update(self, progress, text=None, numDone=None, totalNum=None):
		if not self.Logger.LoadingBarAllowed:
			return
			
		progress = max(progress, 0)
		progress = min(progress, 1)

		progress = int(progress*self.Resolution)

		if time.time()-self.LastUpdateTime >= 0.15 or progress == self.Resolution:

			if progress != self.CurrentProgress or text != self.CurrentText:
				self.Logger.Clear()
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
