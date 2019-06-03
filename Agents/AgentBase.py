import DataManger.BoardInfo as BoardInfo

class AgentBase:

	def __init__(self, dataSetManager, loadData, winningModeON=False):
		self.DataSetManager = dataSetManager
		self.WinningModeON = winningModeON
		self.TempDataSet = {}
		self.RecordMoves = True

		if loadData:
			self.DataSetManager.LoadTableInfo()
		return
	
	def RecordMove(self, board, move):
		if not self.RecordMoves:
			return

		key = self.DataSetManager.BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)


		if found:
			if boardInfo.NumOfTriedMoves < self.DataSetManager.MaxMoveIDs:
				boardInfo.Moves[moveID] = BoardInfo.MoveInfo()
				boardInfo.NumOfTriedMoves += 1

				if boardInfo.NumOfTriedMoves >= self.DataSetManager.MaxMoveIDs:
					self.DataSetManager.MetaData["NumberOfCompleteBoards"] += 1

			else:#played every move once already
				boardInfo.Moves[moveID].TimesPlayed += 1

		else:#never played board before
			self.DataSetManager.AddNewBoard(key, board)

		self.TempDataSet[str(key)+str(moveID)] = {"BoardKey": key, "MoveID": moveID}
		return

	def UpdateInvalidMove(self, board, move):
		if not self.RecordMoves:
			return

		key = self.DataSetManager.BoardToKey(board)
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

		key = self.DataSetManager.BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if found and moveID in boardInfo.Moves:
			if gameFinished:
				outComeKey = "GameFinished"
			else:
				outComeKey = self.DataSetManager.BoardToKey(outComeBoard)

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
