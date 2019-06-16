import DataManger.BoardInfo as BoardInfo
from DataManger.Serializer import BoardToKey


class AgentBase:

	def __init__(self, dataSetManager, loadData, winningModeON=False):
		self.DataSetManager = dataSetManager
		self.WinningModeON = winningModeON
		self.TempDataSet = {}
		self.RecordMoves = True
		
		self.AllMovesPlayedValue = (2**self.DataSetManager.MaxMoveIDs)-1

		if loadData:
			self.DataSetManager.LoadTableInfo()
		return
	
	def RecordMove(self, board, move):
		if not self.RecordMoves:
			return

		key = BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)


		if found:
			# never played this move before
			if moveID not in boardInfo.Moves:
				boardInfo.Moves[moveID] = BoardInfo.MoveInfo()
			else:
				boardInfo.Moves[moveID].TimesPlayed += 1

			# mark move as played if never played before
			if boardInfo.PlayedMovesLookUpArray < self.AllMovesPlayedValue:

				if not (2**moveID & boardInfo.PlayedMovesLookUpArray):
					boardInfo.PlayedMovesLookUpArray += 2**moveID

				if boardInfo.PlayedMovesLookUpArray >= self.AllMovesPlayedValue:
					self.DataSetManager.MetaData["NumberOfCompleteBoards"] += 1


		else:#never played board before
			self.DataSetManager.AddNewBoard(key, board)

		self.TempDataSet[str(key)+str(moveID)] = {"BoardKey": key, "MoveID": moveID}
		return

	def UpdateInvalidMove(self, board, move):
		if not self.RecordMoves:
			return

		key = BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)

		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if found and moveID in boardInfo.Moves:
			del boardInfo.Moves[moveID]

		if str(key)+str(moveID) in self.TempDataSet:
			del self.TempDataSet[str(key)+str(moveID)]
		return

	def UpdateMoveOutCome(self, board, move, outComeBoard, gameFinished=False):
		if not self.RecordMoves:
			return

		key = BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if found and moveID in boardInfo.Moves:
			if gameFinished:
				outComeKey = "GameFinished"
			else:
				outComeKey = BoardToKey(outComeBoard)

			move = boardInfo.Moves[moveID]
			if outComeKey in move.MoveOutComes:
				move.MoveOutComes[outComeKey] += 1
			else:
				move.MoveOutComes[outComeKey] = 1
				
		return

	def SaveData(self, fitness):
		if not self.RecordMoves:
			return
			
		for tempValue in self.TempDataSet.values():
			key = tempValue["BoardKey"]
			moveID = tempValue["MoveID"]

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
