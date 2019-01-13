class Simulation(object):
	Info = {"Name":"TicTacToe",
	        "MinPlayers":2,"MaxPlayers":2,
	        "NumInputs":1,"MinInputSize":0,"MaxInputSize":8,#need to be range until coded so put back
			"Resolution":1}

	def Start(self):

		self.Board = [0,0,0,0,0,0,0,0,0]
		self.Turn = 1
		self.Finished = False
		return self.Board, self.Turn

	def MakeMove(self,inputs):
		valid = False
		if self.Board[inputs[0]] == 0:
			self.Board[inputs[0]] = self.Turn
			valid = True


		if valid:
			if self.Turn == 1:
				self.Turn = 2
			else:
				self.Turn = 1
		return valid, self.Board, self.Turn

	def CheckFinished(self):
		player1Fitness, player2Fitness = 0,0

		if CheckWin(self.Board, 1) == True:#win
			self.Finished = True
			player1Fitness = 5
			player2Fitness = -5

		elif CheckWin(self.Board, 2) == True:#loss
			self.Finished = True
			player1Fitness = -5
			player2Fitness = -5

		elif not(0 in self.Board):#draw
			self.Finished = True
			player1Fitness = 3
			player2Fitness = 3
			

		return self.Finished, [player1Fitness, player2Fitness]

	def FlipBoard(self, board):
		for loop in range(len(board)):
			if board[loop] == 1:
				board[loop] = 2
			elif board[loop] == 2:
				board[loop] = 1

		return board

	def FlipInput(self, move):
		return move

	def SimpleOutput(self, board):
		loop = 0
		for y in range(3):
			temp = ""
			for x in range(3):
				if board[loop] == 0:
					temp += " "
				elif board[loop] == 1:
					temp += "X"
				else:
					temp += "O"

				loop += 1
				if x < 2:
					temp += "|"

			print(temp)
			if y < 2:
				print("-+-+-")
		return

def CheckWin(board, player):
	if    (board[0] == player and board[1] == player and board[2] == player) \
	   or (board[3] == player and board[4] == player and board[5] == player) \
	   or (board[6] == player and board[7] == player and board[8] == player) \
	   or (board[0] == player and board[3] == player and board[6] == player) \
	   or (board[1] == player and board[4] == player and board[7] == player) \
	   or (board[2] == player and board[5] == player and board[8] == player) \
	   or (board[0] == player and board[4] == player and board[8] == player) \
	   or (board[6] == player and board[4] == player and board[2] == player):
		return True

	else:
		return False