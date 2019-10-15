class MoveInfo():
	AvgFitness = 0.0
	TimesPlayed = 1
	MoveOutComes = {}

	def __init__(self, AvgFitness=0.0, TimesPlayed=0):
		self.AvgFitness = AvgFitness
		self.TimesPlayed = TimesPlayed
		self.MoveOutComes = {}
		return