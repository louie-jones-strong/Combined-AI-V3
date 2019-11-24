import RunController.eAgentType as eAgentType

class AgentSetupData:

	def __init__(self, agentType, playingMode=None, subMoveAgent=None, valuePredictor=None, outputPredictor=None):
		self.Type = agentType #enum
		self.PlayingMode = playingMode #enum (winning training)
		self.SubMoveAgent = subMoveAgent #AgentSetupData
		self.ValuePredictor = valuePredictor
		self.OutputPredictor = outputPredictor

		return
	def GetType(self):
		if self.Type == None or self.Type == eAgentType.eAgentType.Null:
			userInput = input("Brute B) Network N) Evolution E) Random R) Human H) MonteCarloAgent M):")
			userInput = userInput.upper()

			if userInput == "B":
				self.Type = eAgentType.eAgentType.BruteForce
			elif userInput == "H":
				self.Type = eAgentType.eAgentType.Human
			elif userInput == "R":
				self.Type = eAgentType.eAgentType.Random
			elif userInput == "N":
				self.Type = eAgentType.eAgentType.NeuralNetwork
			elif userInput == "E":
				self.Type = eAgentType.eAgentType.Evolution
			elif userInput == "M":
				self.Type = eAgentType.eAgentType.MonteCarlo
		
		return self.Type

	def GetPlayingMode(self):
		if self.PlayingMode == None:
			input("pick an PlayingMode")
		
		return self.PlayingMode

	def GetSubMoveAgent(self):
		if self.SubMoveAgent == None:
			self.SubMoveAgent = AgentSetupData(None)
		
		return self.SubMoveAgent

	def GetValuePredictor(self):
		if self.ValuePredictor == None:
			input("pick an ValuePredictor")
		
		return self.ValuePredictor

	def GetOutputPredictor(self):
		if self.OutputPredictor == None:
			input("pick an OutputPredictor")
		
		return self.OutputPredictor