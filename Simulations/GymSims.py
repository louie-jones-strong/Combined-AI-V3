import gym

class Simulation(object):
	Info = {}

	def __init__(self, index=None):
		self.BackGroundpieceList = []

		simsToPickFrom = [
		{"MinPlayers":1,"MaxPlayers":1,"SimName":"CartPole-v1",
		"NumInputs":1,"MinInputSize":0, "MaxInputSize":1,"Resolution":1,"RenderSetup":False},
		{"MinPlayers":1,"MaxPlayers":1,"SimName":"MountainCar-v0",
		"NumInputs":1,"MinInputSize":0, "MaxInputSize":1,"Resolution":1,"RenderSetup":False}]

		if index == None:
			for loop in range(len(simsToPickFrom)):
				print(str(loop)+") "+str(simsToPickFrom[loop]["SimName"]))

			index = int(input("pick Gym Simulation: "))
		self.Index = index
		self.Info = simsToPickFrom[index]

		self.Environment = gym.make(self.Info["SimName"])
		return

	def CreateNew(self):
		sim = Simulation(self.Index)
		return sim
		
	def Start(self):
		self.Finished = False
		self.playerFitness = 0
		board = self.Environment.reset()

		self.Board = []
		for loop in range(len(board)):
			self.Board += [float(board[loop])]

		self.Turn = 1
		return self.Board, self.Turn

	# inputs is an array of size NumInputs
	# Each element of which is between MinInputSize to MaxInputSize
	# and resolution Resolution
	def MakeMove(self,inputs):

		action = inputs[0]
		if action > 0.5:
			action = 1
		else:
			action = 0
		
		if not self.Finished:
			board, temp, self.Finished, _ = self.Environment.step(action)
			self.Board = []
			for loop in range(len(board)):
				self.Board += [float(board[loop])]
			self.playerFitness += temp

		return True, self.Board, self.Turn

	def CheckFinished(self):
		return self.Finished, [self.playerFitness]

	def FlipBoard(self, board):

		return board

	def FlipInput(self, move):
		return move

	def SimpleBoardOutput(self, board):
		self.Environment.render()
		return
	def ComplexBoardOutput(self, board):
		pieceList = []
		pieceList += self.BackGroundpieceList
		return pieceList