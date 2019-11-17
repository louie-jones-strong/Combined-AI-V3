import wandb

class MetricsLogger:
	def __init__(self, projectName):
		self.ProjectName = projectName

		return

	def RunSetup(self, envName):

		runId = envName

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