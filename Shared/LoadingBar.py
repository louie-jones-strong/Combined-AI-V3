import time
import os

class LoadingBar():

	def __init__(self, allowUpdate=True):
		self.CurrentProgress = 0
		self.CurrentText = ""
		self.Resolution = 100
		self.LastUpdateTime = 0
		self.AllowUpdate = allowUpdate
		return

	def Update(self, progress, text=""):
		progress = max(progress, 0)
		progress = min(progress, 1)

		progress = int(progress*self.Resolution)

		if time.time()-self.LastUpdateTime >= 0.15 or progress == self.Resolution:
			if progress != self.CurrentProgress or text != self.CurrentText:
				os.system("cls")
				bar = "#"*progress
				fill = " "*(self.Resolution-progress)
				print("|"+bar+fill+"|")
				print(text)
				self.CurrentProgress = progress
				self.CurrentText = text
				self.LastUpdateTime = time.time()
		return
