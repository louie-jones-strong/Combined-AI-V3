import random
import sys
import BoardInfo

class BruteForce(object): 

	def __init__(self, dataSetManager, winningModeON=False):
		self.DataSetManager = dataSetManager
		self.WinningModeON = winningModeON

		self.TempDataSet = {}
		return

	def MoveCal(self, board):
		key = self.DataSetManager.BoardToKey(board)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if self.WinningModeON:
			print("winnning mode!")
			if found and len(boardInfo.Moves) > 0:
				moveID = boardInfo.MoveIDOfBestAvgFitness

			else:#never played board before
				moveID = random.randint(0,self.DataSetManager.MaxMoveIDs-1)
				print("new Board!")
		else:  # learning mode
			if found:
				if boardInfo.NumOfTriedMoves > self.DataSetManager.MaxMoveIDs:
					if len(boardInfo.Moves) == 0:
						input("error!!!")

				if boardInfo.NumOfTriedMoves < self.DataSetManager.MaxMoveIDs:
					moveID = boardInfo.NumOfTriedMoves
					boardInfo.Moves[moveID] = BoardInfo.MoveInfo()
					boardInfo.NumOfTriedMoves += 1

					if boardInfo.NumOfTriedMoves >= self.DataSetManager.MaxMoveIDs:
						self.DataSetManager.NumberOfCompleteBoards += 1

				else:#played every move once already
					leastPlayed = sys.maxsize
					moveID = 0
					for movekey, moveValue in boardInfo.Moves.items():
						if moveValue.TimesPlayed < leastPlayed:
							leastPlayed = moveValue.TimesPlayed
							moveID = movekey
					
					boardInfo.Moves[moveID].TimesPlayed += 1

			else:#never played board before
				moveID = 0
				self.DataSetManager.AddNewBoard(key, board)

			self.TempDataSet[str(key)+str(moveID)] = {"BoardKey": key, "MoveID": moveID}


		move = self.DataSetManager.MoveIDLookUp[moveID]
		return move

	def UpdateInvalidMove(self, board, move):
		key = self.DataSetManager.BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)

		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if found:
			if moveID in boardInfo.Moves:
				del boardInfo.Moves[moveID]

		if str(key)+str(moveID) in self.TempDataSet:
			del self.TempDataSet[str(key)+str(moveID)]
		return
	
	def SaveData(self, fitness):
		for tempKey in self.TempDataSet:
			key = self.TempDataSet[tempKey]["BoardKey"]
			moveID = self.TempDataSet[tempKey]["MoveID"]

			found, boardInfo = self.DataSetManager.GetBoardInfo(key)
			if found and moveID in boardInfo.Moves:
				newFitness = boardInfo.Moves[moveID].AvgFitness*boardInfo.Moves[moveID].TimesPlayed
				newFitness += fitness
				boardInfo.Moves[moveID].TimesPlayed += 1
				newFitness /= boardInfo.Moves[moveID].TimesPlayed
				boardInfo.Moves[moveID].AvgFitness = newFitness

				if newFitness > boardInfo.BestAvgFitness:
					boardInfo.MoveIDOfBestAvgFitness = moveID
					boardInfo.BestAvgFitness = newFitness



		self.TempDataSet = {}
		return
