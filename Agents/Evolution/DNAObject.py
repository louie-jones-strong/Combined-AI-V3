
class DNAObject:
	Weights = []
	Fittness = 0
	NumberOfGames = 0
	AgentId = None

	def __init__(self, weights):
		self.Weights = weights
		return