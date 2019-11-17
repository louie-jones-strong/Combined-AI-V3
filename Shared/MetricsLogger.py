import wandb

class MetricsLogger:
	def __init__(self, projectName):
		wandb.init(project=projectName)

		return

	def Log(self, key, value):

		self.DictLog({key: value})
		return

	def DictLog(self, logDict):
		wandb.log(logDict)
		return

	def MetricsFolderPath(self):

		return wandb.run.dir