import Shared.BaseMetricsLogger as BaseMetricsLogger
import wandb

class MetricsLogger(BaseMetricsLogger.MetricsLogger):
	def RunSetup(self, runId, resume):
		try:
			wandb.init(project=self.ProjectName, id=runId, resume=resume)
			
		except Exception as e:
			if resume:
				wandb.init(project=self.ProjectName, id=runId, resume=False)

		return

	def Log(self, key, value):

		self.DictLog({key: value})
		return

	def DictLog(self, logDict):
		wandb.log(logDict)
		return

	def MetricsFolderPath(self):

		return wandb.run.dir
