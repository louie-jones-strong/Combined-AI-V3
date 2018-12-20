class Draughts(object):
	def start(self):
		self.Board = self.newBoard()
		self.turn = 1
		self.step = 1
		self.selectedPos = [0,0]
		return self.Board, self.turn

	def newBoard(self):
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

	def MakeSelection(self,X,Y):
		valid = False
		if (self.Board[X][Y] == 1 or self.Board[X][Y] == 3) and self.turn == 1:
			self.selectedPos = [X,Y]
			valid = True

		elif (self.Board[X][Y] == 2 or self.Board[X][Y] == 4) and self.turn == 2:
			self.selectedPos = [X,Y]
			valid = True

		if self.step == 2 and valid:
			for loop in range(8):
				for loop2 in range(8):
					if self.Board[loop][loop2] == -1:
						self.Board[loop][loop2] = 0

		if valid:
			self.step = 2

			moves = self.possibleMoves(X,Y)

			for loop in range(len(moves)):
				self.Board[moves[loop][0]][moves[loop][1]] = -1

		return valid, self.Board
		
	def MakeMove(self,X,Y):
		valid = False
		if self.Board[X][Y] == -1:

			if abs(X - self.selectedPos[0] > 1) or abs(Y - self.selectedPos[1]) > 1:
				output = self.attackMoves(self.selectedPos[0],self.selectedPos[1])
				for loop in range(len(output[0])):
					if output[0][loop][0] == X and output[0][loop][1] == Y:
						temp = output[1][loop]
						self.Board[temp[0]][temp[1]] = 0

			self.Board[X][Y] = self.Board[self.selectedPos[0]][self.selectedPos[1]]
			self.Board[self.selectedPos[0]][self.selectedPos[1]] = 0

			if self.Board[X][Y] == 1 or self.Board[X][Y] == 2:
				if self.Board[X][Y] == 1 and Y == 7:
					self.Board[X][Y] = 3
				elif self.Board[X][Y] == 2 and Y == 0 :
					self.Board[X][Y] = 4

			valid = True
			self.step = 1

		for loop in range(8):
			for loop2 in range(8):
				if self.Board[loop][loop2] == -1:
					self.Board[loop][loop2] = 0

		if valid:
			if self.turn == 1:
				self.turn = 2
			else:
				self.turn = 1
		return valid, self.Board, self.turn

	def attackMoves(self,X,Y):
		outputList = []
		ToRemoveList = []
		piece = self.Board[X][Y]

		if self.Board[X][Y] == 3 or self.Board[X][Y] == 4:

			if X >= 2 and Y >= 2:
				if IsPieceEnemySide(piece, self.Board[X-1][Y-1]) and (self.Board[X-2][Y-2] == 0 or self.Board[X-2][Y-2] == -1):
					outputList += [[X-2,Y-2]]
					ToRemoveList += [[X-1,Y-1]]
			if X <= 5 and Y >= 2:
				if IsPieceEnemySide(piece, self.Board[X+1][Y-1]) and (self.Board[X+2][Y-2] == 0 or self.Board[X+2][Y-2] == -1):
					outputList += [[X+2,Y-2]]
					ToRemoveList += [[X+1,Y-1]]
			if X >= 2 and Y <= 5:
				if IsPieceEnemySide(piece, self.Board[X-1][Y+1]) and (self.Board[X-2][Y+2] == 0 or self.Board[X-2][Y+2] == -1):
					outputList += [[X-2,Y+2]]
					ToRemoveList += [[X-1,Y+1]]
			if X <= 5 and Y <= 5:
				if IsPieceEnemySide(piece, self.Board[X+1][Y+1]) and (self.Board[X+2][Y+2] == 0 or self.Board[X+2][Y+2] == -1):
					outputList += [[X+2,Y+2]]
					ToRemoveList += [[X+1,Y+1]]

		elif self.Board[X][Y] == 1 or self.Board[X][Y] == 3:

			if X >= 2 and Y <= 5:
				if IsPieceEnemySide(piece, self.Board[X-1][Y+1]) and (self.Board[X-2][Y+2] == 0 or self.Board[X-2][Y+2] == -1):
					outputList += [[X-2,Y+2]]
					ToRemoveList += [[X-1,Y+1]]
			if X <= 5 and Y <= 5:
				if IsPieceEnemySide(piece, self.Board[X+1][Y+1]) and (self.Board[X+2][Y+2] == 0 or self.Board[X+2][Y+2] == -1):
					outputList += [[X+2,Y+2]]
					ToRemoveList += [[X+1,Y+1]]

		elif self.Board[X][Y] == 2 or self.Board[X][Y] == 4:

			if X >= 2 and Y >= 2:
				if IsPieceEnemySide(piece, self.Board[X-1][Y-1]) and (self.Board[X-2][Y-2] == 0 or self.Board[X-2][Y-2] == -1):
					outputList += [[X-2,Y-2]]
					ToRemoveList += [[X-1,Y-1]]
			if X <= 5 and Y >= 2:
				if IsPieceEnemySide(piece, self.Board[X+1][Y-1]) and (self.Board[X+2][Y-2] == 0 or self.Board[X+2][Y-2] == -1):
					outputList += [[X+2,Y-2]]
					ToRemoveList += [[X+1,Y-1]]

		return outputList, ToRemoveList
	
	def possibleMoves(self,X,Y):
		outputList = self.attackMoves(X,Y)[0]
		if len(outputList) == 0:

			if self.Board[X][Y] == 3 or self.Board[X][Y] == 4:

				if X >= 1 and Y >= 1:
					if self.Board[X-1][Y-1] == 0:
						outputList += [[X-1,Y-1]]
				if X <= 6 and Y >= 1:
					if self.Board[X+1][Y-1] == 0:
						outputList += [[X+1,Y-1]]
				if X >= 1 and Y <= 6:
					if self.Board[X-1][Y+1] == 0:
						outputList += [[X-1,Y+1]]
				if X <= 6 and Y <= 6:
					if self.Board[X+1][Y+1] == 0:
						outputList += [[X+1,Y+1]]

			elif self.Board[X][Y] == 1:

				if X >= 1 and Y <= 6:
					if self.Board[X-1][Y+1] == 0:
						outputList += [[X-1,Y+1]]
				if X <= 6 and Y <= 6:
					if self.Board[X+1][Y+1] == 0:
						outputList += [[X+1,Y+1]]

			elif self.Board[X][Y] == 2:

				if X >= 1 and Y >= 1:
					if self.Board[X-1][Y-1] == 0:
						outputList += [[X-1,Y-1]]
				if X <= 6 and Y >= 1:
					if self.Board[X+1][Y-1] == 0:
						outputList += [[X+1,Y-1]]


		return outputList

	def CheckIfDrawed(self):
		type1Moves = 0
		type2Moves = 0
		for x in range(len(self.Board)):
			for y in range(len(self.Board[x])):
				if IsPieceSameSide(self.Board[x][y], 1):
					if self.possibleMoves(x,y):
						type1Moves += 1

				elif IsPieceSameSide(self.Board[x][y], 2):
					if self.possibleMoves(x,y):
						type2Moves += 1

		if type1Moves == 0 or type2Moves == 0:
			return True
		return False

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

		if self.CheckIfDrawed():
			finished = True
			player1Fitness = 3
			player2Fitness = 3



		return finished, [player1Fitness, player2Fitness]

	def FlipBoard(self):
		output = []
		for loop in range(len(self.Board)-1,-1,-1):
			temp = []
			for loop2 in range(len(self.Board[loop])-1,-1,-1):
				piece = self.Board[loop][loop2]

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

def SimpleOutput(board):
	for loop in range(len(board)):
		temp = ""
		for loop2 in range(len(board[loop])):
			if board[loop2][loop] == 0:
				temp += "  "
			else:
				temp += "" + str(board[loop2][loop]) + " "
		print(temp)
	return

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

#todo list 
#1) must take peice
#2) take more then one peice at once