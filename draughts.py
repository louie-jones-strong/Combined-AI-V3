class game(object):
	def start(self):
		self.Board = self.newBoard()
		self.turn = 2
		self.step = 1
		self.selectedPos = [0,0]
		return self.Board, self.turn, 1

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

	def selection(self,X,Y):
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

		return valid, self.Board, self.step
		
	def moveCal(self,X,Y):
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
		return valid, self.Board, self.turn, self.step

	def attackMoves(self,X,Y):
		outputList = []
		ToRemoveList = []

		if self.Board[X][Y] == 1 or self.Board[X][Y] == 3:
			enemyType = 2
		else:
			enemyType = 1

		if self.Board[X][Y] == 3 or self.Board[X][Y] == 4:

			if X >= 2 and Y >= 2:
				if self.Board[X-1][Y-1] == enemyType and (self.Board[X-2][Y-2] == 0 or self.Board[X-2][Y-2] == -1):
					outputList += [[X-2,Y-2]]
					ToRemoveList += [[X-1,Y-1]]
			if X <= 5 and Y >= 2:
				if self.Board[X+1][Y-1] == enemyType and (self.Board[X+2][Y-2] == 0 or self.Board[X+2][Y-2] == -1):
					outputList += [[X+2,Y-2]]
					ToRemoveList += [[X+1,Y-1]]
			if X >= 2 and Y <= 5:
				if self.Board[X-1][Y+1] == enemyType and (self.Board[X-2][Y+2] == 0 or self.Board[X-2][Y+2] == -1):
					outputList += [[X-2,Y+2]]
					ToRemoveList += [[X-1,Y+1]]
			if X <= 5 and Y <= 5:
				if self.Board[X+1][Y+1] == enemyType and (self.Board[X+2][Y+2] == 0 or self.Board[X+2][Y+2] == -1):
					outputList += [[X+2,Y+2]]
					ToRemoveList += [[X+1,Y+1]]

		elif self.Board[X][Y] == 1 or self.Board[X][Y] == 3:

			if X >= 2 and Y <= 5:
				if self.Board[X-1][Y+1] == enemyType and (self.Board[X-2][Y+2] == 0 or self.Board[X-2][Y+2] == -1):
					outputList += [[X-2,Y+2]]
					ToRemoveList += [[X-1,Y+1]]
			if X <= 5 and Y <= 5:
				if self.Board[X+1][Y+1] == enemyType and (self.Board[X+2][Y+2] == 0 or self.Board[X+2][Y+2] == -1):
					outputList += [[X+2,Y+2]]
					ToRemoveList += [[X+1,Y+1]]

		elif self.Board[X][Y] == 2 or self.Board[X][Y] == 4:

			if X >= 2 and Y >= 2:
				if self.Board[X-1][Y-1] == enemyType and (self.Board[X-2][Y-2] == 0 or self.Board[X-2][Y-2] == -1):
					outputList += [[X-2,Y-2]]
					ToRemoveList += [[X-1,Y-1]]
			if X <= 5 and Y >= 2:
				if self.Board[X+1][Y-1] == enemyType and (self.Board[X+2][Y-2] == 0 or self.Board[X+2][Y-2] == -1):
					outputList += [[X+2,Y-2]]
					ToRemoveList += [[X+1,Y-1]]

		return outputList, ToRemoveList
	
def IsEnemyType(allyType, piece):
	if (allyType == 1 or allyType == 3) and (piece == 2 or piece == 4):
		return True
	elif (allyType == 2 or allyType == 4) and (piece == 1 or piece == 3):
		return True
	return False

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

	def FlipBoard(self):

		output = []

		for loop in range(len(self.Board)):
			temp = []
			for loop2 in range(len(self.Board[loop])):
				if self.Board[loop][loop2] == 1:
					temp += [2]
				elif self.Board[loop][loop2] == 2:
					temp += [1]
				elif self.Board[loop][loop2] == 3:
					temp += [4]
				elif self.Board[loop][loop2] == 4:
					temp += [3]
				else:
					temp += [self.Board[loop][loop2]]
					
			output += [temp]
		return output

def IsPieceSameSide(piece1, piece2):
	if (piece1 == 1 or piece1 == 3) and (piece2 == 1 or piece2 == 3):
		return True

	elif (piece1 == 2 or piece1 == 4) and (piece2 == 2 or piece2 == 4):
		return True
		
	return False