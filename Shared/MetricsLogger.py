import wandb
import Shared.OutputFormating as Format
import time

class MetricsLogger:
	def __init__(self, projectName):
		self.ProjectName = projectName

		return

	def RunSetup(self, envName):

		runId = envName +"_"+ Format.TimeToDateTime(time.time(),True, True, 
			dateSplitter="_", timeSplitter="_", dateTimeSplitter="_")

		wandb.init(project=self.ProjectName, id=runId)
		return

	def Log(self, key, value):

		self.DictLog({key: value})
		return

	def DictLog(self, logDict):
		wandb.log(logDict)
		return

	def MetricsFolderPath(self):

		return wandb.run.dir