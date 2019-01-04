class Simulation(object):
	Info = {"Name":"Draughts",
	        "MinPlayers":2,"MaxPlayers":2,
	        "NumInputs":4,"MinInputSize":0,"MaxInputSize":7,
			"Resolution":1}
	
	def Start(self):
		self.Board = NewBoard()
		self.Turn = 1
		return self.Board, self.Turn
		
	def MakeMove(self,moveArray):
		valid = False
		if (self.Board[moveArray[0]][moveArray[1]] == 1 or self.Board[moveArray[0]][moveArray[1]] == 3) and self.Turn == 1:
			selectedPos = [moveArray[0],moveArray[1]]
			valid = True

		elif (self.Board[moveArray[0]][moveArray[1]] == 2 or self.Board[moveArray[0]][moveArray[1]] == 4) and self.Turn == 2:
			selectedPos = [moveArray[0],moveArray[1]]
			valid = True

		if valid:
			moves = PossibleMoves(self.Board, moveArray[0], moveArray[1])

			if len(moves) == 0:
				return False, self.Board, self.Turn

			for loop in range(len(moves)):
				self.Board[moves[loop][0]][moves[loop][1]] = -1
		else:
			return valid, self.Board, self.Turn

		#move
		valid = False
		if self.Board[moveArray[2]][moveArray[3]] == -1:

			if abs(moveArray[2] - selectedPos[0] > 1) or abs(moveArray[3] - selectedPos[1]) > 1:
				output = AttackMoves(self.Board, selectedPos[0], selectedPos[1])
				for loop in range(len(output[0])):
					if output[0][loop][0] == moveArray[2] and output[0][loop][1] == moveArray[3]:
						temp = output[1][loop]
						self.Board[temp[0]][temp[1]] = 0

			self.Board[moveArray[2]][moveArray[3]] = self.Board[selectedPos[0]][selectedPos[1]]
			self.Board[selectedPos[0]][selectedPos[1]] = 0

			if self.Board[moveArray[2]][moveArray[3]] == 1 or self.Board[moveArray[2]][moveArray[3]] == 2:
				if self.Board[moveArray[2]][moveArray[3]] == 1 and moveArray[3] == 7:
					self.Board[moveArray[2]][moveArray[3]] = 3
				elif self.Board[moveArray[2]][moveArray[3]] == 2 and moveArray[3] == 0 :
					self.Board[moveArray[2]][moveArray[3]] = 4

			valid = True

		for loop in range(8):
			for loop2 in range(8):
				if self.Board[loop][loop2] == -1:
					self.Board[loop][loop2] = 0

		if valid:
			if self.Turn == 1:
				self.Turn = 2
			else:
				self.Turn = 1
		return valid, self.Board, self.Turn

	def CheckFinished(self):
		finished = False
		player1Fitness = 0
		player2Fitness = 0

		type1Count = 0
		type2Count = 0
		for x in range(len(self.Board)):
			for y in range(len(self.Board[x])):
				if self.Board[x][y] == 1 or self.Board[x][y] == 3:
					 type1Count += 1
				elif self.Board[x][y] == 2 or self.Board[x][y] == 4:
					type2Count += 1
		
		if type1Count == 0:
			finished = True
			player1Fitness = -5
			player2Fitness = 5

		if type2Count == 0:
			finished = True
			player1Fitness = 5
			player2Fitness = -5

		if CheckIfDrawed(self.Board):
			finished = True
			player1Fitness = 3
			player2Fitness = 3



		return finished, [player1Fitness, player2Fitness]

	def FlipBoard(self, board):
		output = []
		for loop in range(len(board)-1,-1,-1):
			temp = []
			for loop2 in range(len(board[loop])-1,-1,-1):
				piece = board[loop][loop2]

				if piece == 1:
					temp += [2]
				elif piece == 2:
					temp += [1]
				elif piece == 3:
					temp += [4]
				elif piece == 4:
					temp += [3]
				else:
					temp += [piece]

			output += [temp]

		return output

	def FlipInput(self, move):
		temp = [7-move[0], 7-move[1], 7-move[2], 7-move[3]]
		return temp

def CheckIfDrawed(board):
	type1Moves = 0
	type2Moves = 0
	for x in range(len(board)):
		for y in range(len(board[x])):
			if IsPieceSameSide(board[x][y], 1):
				if PossibleMoves(board, x, y):
					type1Moves += 1
			elif IsPieceSameSide(board[x][y], 2):
				if PossibleMoves(board, x, y):
					type2Moves += 1
	if type1Moves == 0 or type2Moves == 0:
		return True
	return False

def PossibleMoves(board, X, Y):
	outputList = AttackMoves(board,X,Y)[0]
	if len(outputList) == 0:
		if board[X][Y] == 3 or board[X][Y] == 4:
			if X >= 1 and Y >= 1:
				if board[X-1][Y-1] == 0:
					outputList += [[X-1,Y-1]]
			if X <= 6 and Y >= 1:
				if board[X+1][Y-1] == 0:
					outputList += [[X+1,Y-1]]
			if X >= 1 and Y <= 6:
				if board[X-1][Y+1] == 0:
					outputList += [[X-1,Y+1]]
			if X <= 6 and Y <= 6:
				if board[X+1][Y+1] == 0:
					outputList += [[X+1,Y+1]]
		elif board[X][Y] == 1:
			if X >= 1 and Y <= 6:
				if board[X-1][Y+1] == 0:
					outputList += [[X-1,Y+1]]
			if X <= 6 and Y <= 6:
				if board[X+1][Y+1] == 0:
					outputList += [[X+1,Y+1]]
		elif board[X][Y] == 2:
			if X >= 1 and Y >= 1:
				if board[X-1][Y-1] == 0:
					outputList += [[X-1,Y-1]]
			if X <= 6 and Y >= 1:
				if board[X+1][Y-1] == 0:
					outputList += [[X+1,Y-1]]
	return outputList
		
def AttackMoves(board, X, Y):
	outputList = []
	ToRemoveList = []
	piece = board[X][Y]
	if board[X][Y] == 3 or board[X][Y] == 4:
		if X >= 2 and Y >= 2:
			if IsPieceEnemySide(piece, board[X-1][Y-1]) and (board[X-2][Y-2] == 0 or board[X-2][Y-2] == -1):
				outputList += [[X-2,Y-2]]
				ToRemoveList += [[X-1,Y-1]]
		if X <= 5 and Y >= 2:
			if IsPieceEnemySide(piece, board[X+1][Y-1]) and (board[X+2][Y-2] == 0 or board[X+2][Y-2] == -1):
				outputList += [[X+2,Y-2]]
				ToRemoveList += [[X+1,Y-1]]
		if X >= 2 and Y <= 5:
			if IsPieceEnemySide(piece, board[X-1][Y+1]) and (board[X-2][Y+2] == 0 or board[X-2][Y+2] == -1):
				outputList += [[X-2,Y+2]]
				ToRemoveList += [[X-1,Y+1]]
		if X <= 5 and Y <= 5:
			if IsPieceEnemySide(piece, board[X+1][Y+1]) and (board[X+2][Y+2] == 0 or board[X+2][Y+2] == -1):
				outputList += [[X+2,Y+2]]
				ToRemoveList += [[X+1,Y+1]]
	elif board[X][Y] == 1 or board[X][Y] == 3:
		if X >= 2 and Y <= 5:
			if IsPieceEnemySide(piece, board[X-1][Y+1]) and (board[X-2][Y+2] == 0 or board[X-2][Y+2] == -1):
				outputList += [[X-2,Y+2]]
				ToRemoveList += [[X-1,Y+1]]
		if X <= 5 and Y <= 5:
			if IsPieceEnemySide(piece, board[X+1][Y+1]) and (board[X+2][Y+2] == 0 or board[X+2][Y+2] == -1):
				outputList += [[X+2,Y+2]]
				ToRemoveList += [[X+1,Y+1]]
	elif board[X][Y] == 2 or board[X][Y] == 4:
		if X >= 2 and Y >= 2:
			if IsPieceEnemySide(piece, board[X-1][Y-1]) and (board[X-2][Y-2] == 0 or board[X-2][Y-2] == -1):
				outputList += [[X-2,Y-2]]
				ToRemoveList += [[X-1,Y-1]]
		if X <= 5 and Y >= 2:
			if IsPieceEnemySide(piece, board[X+1][Y-1]) and (board[X+2][Y-2] == 0 or board[X+2][Y-2] == -1):
				outputList += [[X+2,Y-2]]
				ToRemoveList += [[X+1,Y-1]]
	return outputList, ToRemoveList

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

#todo list 
#1) take more then one peice at once