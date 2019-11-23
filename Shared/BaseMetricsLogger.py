
class MetricsLogger:
	def __init__(self, projectName, metricsOn):
		self.ProjectName = projectName
		self.MetricsOn = metricsOn

		return

	def RunSetup(self, runId, resume):
		if not self.MetricsOn:
			return
		return

	def Log(self, key, value):
		if not self.MetricsOn:
			return
		return

	def DictLog(self, logDict):
		if not self.MetricsOn:
			return
		return

	def MetricsFolderPath(self):
		if not self.MetricsOn:
			return

		return
