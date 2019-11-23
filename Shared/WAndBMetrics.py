import Shared.BaseMetricsLogger as BaseMetricsLogger
import wandb

class MetricsLogger(BaseMetricsLogger.MetricsLogger):
	def RunSetup(self, runId, resume):
		super().RunSetup(runId, resume)
		if not self.MetricsOn:
			return

		try:
			wandb.init(project=self.ProjectName, id=runId, resume=resume)
			
		except Exception as e:
			if resume:
				wandb.init(project=self.ProjectName, id=runId, resume=False)

		return

	def Log(self, key, value):
		super().Log(key, value)
		if not self.MetricsOn:
			return

		self.DictLog({key: value})
		return

	def DictLog(self, logDict):
		super().DictLog(logDict)
		if not self.MetricsOn:
			return

		wandb.log(logDict)
		return

	def MetricsFolderPath(self):
		super().MetricsFolderPath()
		if not self.MetricsOn:
			return

		return wandb.run.dir
