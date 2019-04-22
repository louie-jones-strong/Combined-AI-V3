class Simulation(object):
	Info = {"MinPlayers":1,"MaxPlayers":2,
	        "NumInputs":1,"MinInputSize":1,"MaxInputSize":3,
			"Resolution":0.1}

	def Start(self, numPlayers):
		if numPlayers > self.Info["MaxPlayers"] or numPlayers < self.Info["MinPlayers"]:
			self.Finished = True
			input("ERROR!! "+str(numPlayers))
		else:
			self.Finished = False

		self.Board = []
		self.Turn = 1
		self.NumPlayers = numPlayers
		return self.Board, self.Turn

	# inputs is an array of size NumInputs
	# Each element of which is between MinInputSize to MaxInputSize
	# and resolution Resolution
	def MakeMove(self,inputs):
		valid = False
		# remember to update turn and board
		return valid, self.Board, self.Turn

	def CheckFinished(self):
		player1Fitness, player2Fitness = 0,0
		return self.Finished, [player1Fitness, player2Fitness]

	def FlipBoard(self, board):

		return board

	def FlipInput(self, move):
		return move

	def SimpleBoardOutput(self, board):
		
		return