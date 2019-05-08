import gym
class Simulation(object):
	Info = {"MinPlayers":1,"MaxPlayers":1,
	        "NumInputs":1,"MinInputSize":0,"MaxInputSize":1,
			"Resolution":1}

	def __init__(self):
		self.BackGroundpieceList = []
		self.Environment = gym.make("CartPole-v1")
		return
		
	def Start(self):
		self.Finished = False
		self.playerFitness = 0
		board = self.Environment.reset()

		self.Board = [board[0], board[1], board[2], board[3]]

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
			self.Board = [board[0], board[1], board[2], board[3]]
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

