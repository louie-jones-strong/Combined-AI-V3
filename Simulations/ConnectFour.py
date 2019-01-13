class Simulation(object):
	Info = {"Name":"ConnectFour",
	        "MinPlayers":2,"MaxPlayers":2,
	        "NumInputs":1,"MinInputSize":0,"MaxInputSize":6,
			"Resolution":1}

	def Start(self):
		self.Board = [[0,0,0,0,0,0],[0,0,0,0,0,0],
					[0,0,0,0,0,0],[0,0,0,0,0,0],
					[0,0,0,0,0,0],[0,0,0,0,0,0],
					[0,0,0,0,0,0]]
		self.Turn = 1
		self.MoveNum = 0
		self.Finished = False
		return self.Board, self.Turn

	def MakeMove(self,inputs):
		valid = False

		column = inputs[0]

		if self.Board[column][0] == 0:
			temp = 0
			valid = True
			for loop in range(1,len(self.Board[column])):

				if (self.Board[column][loop] == 0):
					temp = loop
				else:
					break
			
			self.Board[column][temp] = self.Turn
				
		
		if valid:
			if self.Turn == 1:
				self.Turn = 2
			else:
				self.Turn = 1

			self.MoveNum += 1
		return valid, self.Board, self.Turn

	def CheckFinished(self):
		player1Fitness, player2Fitness = 0,0

		if self.MoveNum >= 7:
			won, side = WinCheck(self.Board)
			if won:
				if (side == 1):#win
					self.Finished = True
					player1Fitness = 5
					player2Fitness = -5

				elif (side == 2):#loss
					self.Finished = True
					player1Fitness = -5
					player2Fitness = 5

				elif side == 0:#draw
					self.Finished = True
					player1Fitness = 3
					player2Fitness = 3
			
		return self.Finished, [player1Fitness, player2Fitness]

	def FlipBoard(self, board):
		output = []
		for X in range(len(board)):
			temp = []
			for Y in range(len(board[X])):
				if board[X][Y] == 1:
					temp += [2]
				elif board[X][Y] == 2:
					temp += [1]
				else:
					temp += [0]

			output += [temp]

		return output

	def FlipInput(self, move):
		return move

	def SimpleOutput(self, board):
		for Y in range(len(board[0])):
			temp = "|"
			for X in range(len(board)):
				if board[X][Y] == 1:
					temp += "O"
				elif board[X][Y] == 2:
					temp += "X"
				else:
					temp += " "
				temp += "|"

			print(temp)
		return

def WinCheck(board):
	won = False
	side = 0
	foundZero = False
	for X in range(len(board)):
		for Y in range(len(board[X])):

			if board[X][Y] != 0:
				for turn in [1,2]:
					if X < len(board)-3:
						if board[X][Y] == turn and board[X+1][Y] == turn \
						and board[X+2][Y] == turn and board[X+3][Y] == turn:
							won = True
							side = turn
							return won, side

						if Y < len(board[X])-3:
							if board[X][Y] == turn and board[X+1][Y+1] == turn \
							and board[X+2][Y+2] == turn and board[X+3][Y+3] == turn:
								won = True
								side = turn
								return won, side

					if Y < len(board[X])-3:
						if board[X][Y] == turn and board[X][Y+1] == turn \
						and board[X][Y+2] == turn and board[X][Y+3] == turn:
							won = True
							side = turn
							return won, side

					if X > 2:
						if Y > 2:
							if board[X][Y] == turn and board[X-1][Y-1] == turn \
							and board[X-2][Y-2] == turn and board[X-3][Y-3] == turn:
								won = True
								side = turn
								return won, side
			
			else:
				foundZero = True

				
	if not won and not foundZero:
		won = True
		side = 0

	return won, side