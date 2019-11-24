

class AgentType:

	def __init__(self, aiType, playingMode, subMoveAgent=None, valuePredictor=None, outputPredictor=None):
		self.AiType = aiType #enum
		self.PlayingMode = playingMode #enum (winning training)
		self.SubMoveAgent = subMoveAgent #agenttype
		self.ValuePredictor = valuePredictor
		self.OutputPredictor = outputPredictor

		return
	def GetAiType(self):
		if self.AiType == None:
			input("pick an AiType")
		
		return self.AiType

	def GetPlayingMode(self):
		if self.PlayingMode == None:
			input("pick an PlayingMode")
		
		return self.PlayingMode

	def GetSubMoveAgent(self):
		if self.SubMoveAgent == None:
			input("pick an ai")
		
		return self.SubMoveAgent

	def GetValuePredictor(self):
		if self.ValuePredictor == None:
			input("pick an ValuePredictor")
		
		return self.ValuePredictor

	def GetOutputPredictor(self):
		if self.OutputPredictor == None:
			input("pick an OutputPredictor")
		
		return self.OutputPredictor