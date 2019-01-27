class Simulation(object):
	Info = {"MinPlayers":2,"MaxPlayers":2,
	        "NumInputs":4,"MinInputSize":0,"MaxInputSize":7,
			"Resolution":1}
	
	def Start(self):
		self.Board = NewBoard()
		self.Turn = 1
		self.NumMoves = 0
		self.CanMoveAgain = None
		return self.Board, self.Turn
		
	def MakeMove(self,moveArray):
		selectedPiece = int(self.Board[moveArray[0]][moveArray[1]])

		if [moveArray[0],moveArray[1]] == self.CanMoveAgain \
			and [moveArray[2],moveArray[3]] == self.CanMoveAgain:
			self.NumMoves += 1
			self.CanMoveAgain = None
			if self.Turn == 1:
				self.Turn = 2
			else:
				self.Turn = 1
			return True, self.Board, self.Turn

		if self.Board[moveArray[2]][moveArray[3]] != 0:
			return False, self.Board, self.Turn

		#check if your pick one of your pieces
		if not(((selectedPiece == 1 or selectedPiece == 3) and self.Turn == 1) \
		or ((selectedPiece == 2 or selectedPiece == 4) and self.Turn == 2)):
			return False, self.Board, self.Turn

		moves = PossibleMoves(self.Board, moveArray[0], moveArray[1])
		if len(moves) == 0:
			return False, self.Board, self.Turn

		if not([moveArray[2],moveArray[3]] in moves):
			return False, self.Board, self.Turn

		#move the piece
		self.Board[moveArray[2]][moveArray[3]] = selectedPiece
		self.Board[moveArray[0]][moveArray[1]] = 0

		canMoveAgain = False
		#check if attack move if so remove piece in the middle
		if abs(moveArray[2] - moveArray[0]) > 1 or abs(moveArray[3] - moveArray[1]) > 1:
			temp = [moveArray[0]+int((moveArray[2]-moveArray[0])/2),moveArray[1]+int((moveArray[3]-moveArray[1])/2)]
			self.Board[temp[0]][temp[1]] = 0

			if len(AttackMoves(self.Board, moveArray[2], moveArray[3])) > 0:
				canMoveAgain = True
				self.CanMoveAgain = [moveArray[2],moveArray[3]]


		#upgrade the piece
		if selectedPiece == 1 and moveArray[3] == 7:
			self.Board[moveArray[2]][moveArray[3]] = 3

		elif selectedPiece == 2 and moveArray[3] == 0 :
			self.Board[moveArray[2]][moveArray[3]] = 4


		if not canMoveAgain:
			self.NumMoves += 1
			self.CanMoveAgain = None
			if self.Turn == 1:
				self.Turn = 2
			else:
				self.Turn = 1
		return True, self.Board, self.Turn

	def CheckFinished(self):
		finished = False
		player1Fitness = 0
		player2Fitness = 0

		type1Count = 0
		type2Count = 0

		type1Moves = 0
		type2Moves = 0

		for x in range(len(self.Board)):
			for y in range(len(self.Board[x])):

				if IsPieceSameSide(self.Board[x][y], 1):
					type1Count += 1
					if PossibleMoves(self.Board, x, y):
						type1Moves += 1

				elif IsPieceSameSide(self.Board[x][y], 2):
					type2Count += 1
					if PossibleMoves(self.Board, x, y):
						type2Moves += 1
		
		if type1Count == 0 or type1Moves == 0:
			finished = True
			player1Fitness = -5
			player2Fitness = 5

		if type2Count == 0 or type2Moves == 0:
			finished = True
			player1Fitness = 5
			player2Fitness = -5

		#check if progress in last 50 moves if not then draw
		if self.NumMoves >= 1000:
			finished = True
			player1Fitness = 3
			player2Fitness = 3



		return finished, [player1Fitness, player2Fitness]

	def FlipBoard(self, board):
		lookup = {0:0,1:2,2:1,3:4,4:3}
		output = []
		for loop in range(len(board)-1,-1,-1):
			temp = []
			for loop2 in range(len(board[loop])-1,-1,-1):
				temp += [lookup[board[loop][loop2]]]
			output += [temp]

		return output

	def FlipInput(self, move):
		temp = [7-move[0], 7-move[1], 7-move[2], 7-move[3]]
		return temp

	def SimpleOutput(self, board):
		for loop in range(len(board)):
			temp = ""
			for loop2 in range(len(board[loop])):
				if (board[loop2][loop] == 0):
					temp += "  "
				else:
					temp += str(board[loop2][loop])
				
			print(temp)
		return

def PossibleMoves(board, X, Y):
	outputList = AttackMoves(board,X,Y)

	if board[X][Y] != 2:
		if X >= 1 and Y <= 6:
			if board[X-1][Y+1] == 0:
				outputList += [[X-1,Y+1]]
		if X <= 6 and Y <= 6:
			if board[X+1][Y+1] == 0:
				outputList += [[X+1,Y+1]]

	if board[X][Y] != 1:
		if X >= 1 and Y >= 1:
			if board[X-1][Y-1] == 0:
				outputList += [[X-1,Y-1]]
		if X <= 6 and Y >= 1:
			if board[X+1][Y-1] == 0:
				outputList += [[X+1,Y-1]]

	return outputList
		
def AttackMoves(board, X, Y):
	outputList = []
	piece = int(board[X][Y])

	if board[X][Y] != 2:
		if X >= 2 and Y <= 5:
			if IsPieceEnemySide(piece, board[X-1][Y+1]) and board[X-2][Y+2] == 0:
				outputList += [[X-2,Y+2]]

		if X <= 5 and Y <= 5:
			if IsPieceEnemySide(piece, board[X+1][Y+1]) and board[X+2][Y+2] == 0:
				outputList += [[X+2,Y+2]]

	if board[X][Y] != 1:
		if X >= 2 and Y >= 2:
			if IsPieceEnemySide(piece, board[X-1][Y-1]) and board[X-2][Y-2] == 0:
				outputList += [[X-2,Y-2]]

		if X <= 5 and Y >= 2:
			if IsPieceEnemySide(piece, board[X+1][Y-1]) and board[X+2][Y-2] == 0:
				outputList += [[X+2,Y-2]]

	return outputList

def IsPieceSameSide(piece1, piece2):
	if (piece1 == 1 or piece1 == 3) and (piece2 == 1 or piece2 == 3):
		return True

	elif (piece1 == 2 or piece1 == 4) and (piece2 == 2 or piece2 == 4):
		return True
		
	return False

def IsPieceEnemySide(piece1, piece2):
	if (piece1 == 1 or piece1 == 3) and (piece2 == 2 or piece2 == 4):
		return True

	elif (piece1 == 2 or piece1 == 4) and (piece2 == 1 or piece2 == 3):
		return True
		
	return False

def NewBoard():
	Board = []
	pickColour = 1
	for loop in range(8):
		test2 = []
		for loop2 in range(8):
			if pickColour == 1 :
				if loop2 < 3 :
					test2 += [1]
				elif loop2>4:
					test2 += [2]
				else:
					test2 += [0]
				pickColour = 2
			else:
				test2 += [0]
				pickColour = 1

		if pickColour == 1:
			pickColour = 2
		else:
			pickColour = 1
		Board += [test2]

	return Board
