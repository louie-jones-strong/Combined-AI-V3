import DataManger.BoardInfo as BoardInfo
from DataManger.Serializer import BoardToKey


class AgentBase:
	AgentType = "Base"
	InvalidMoveList = {}
	
	def __init__(self, dataSetManager, loadData, winningModeON=False):
		self.DataSetManager = dataSetManager
		self.WinningModeON = winningModeON
		self.TempDataSet = {}
		self.MoveNumber = 0
		self.RecordMoves = True
		
		self.AllMovesPlayedValue = (2**self.DataSetManager.MaxMoveIDs)-1

		if loadData:
			self.DataSetManager.LoadTableInfo()
		return
	
	def RecordMove(self, board, move):
		if not self.RecordMoves:
			return

		self.DataSetManager.MetaDataAdd("TriedMovesPlayed", 1)

		key = BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if not found:  # never played board before
			self.DataSetManager.AddNewBoard(key, board)
			found, boardInfo = self.DataSetManager.GetBoardInfo(key)
		
		with boardInfo.Lock:
			boardInfo.BeingUsed = True
			# never played this move before
			if moveID not in boardInfo.Moves:
				boardInfo.Moves[moveID] = BoardInfo.MoveInfo()

			# mark move as played if never played before
			if boardInfo.PlayedMovesLookUpArray < self.AllMovesPlayedValue:

				if not (2**moveID & boardInfo.PlayedMovesLookUpArray):
					boardInfo.PlayedMovesLookUpArray += 2**moveID

				if boardInfo.PlayedMovesLookUpArray >= self.AllMovesPlayedValue:
					self.DataSetManager.MetaDataAdd("NumberOfCompleteBoards", 1)
				

		if self.RecordMoves:
			self.TempDataSet[str(key)+str(moveID)] = {"BoardKey": key, "MoveID": moveID, "MoveNumber":self.MoveNumber}
			self.MoveNumber += 1

		if key not in self.InvalidMoveList:
			self.InvalidMoveList[key] = 0
		return

	def UpdateInvalidMove(self, board, move):
		if not self.RecordMoves:
			return

		key = BoardToKey(board)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)

		found, boardInfo = self.DataSetManager.GetBoardInfo(key)
		with boardInfo.Lock:
			if found and moveID in boardInfo.Moves:
				del boardInfo.Moves[moveID]

		if str(key)+str(moveID) in self.TempDataSet:
			del self.TempDataSet[str(key)+str(moveID)]

		self.MoveNumber -= 1

		self.InvalidMoveList[key] += 1
		return

	def UpdateMoveOutCome(self, boardKey, move, outComeBoard, gameFinished=False):
		if not self.RecordMoves:
			return
		
		self.DataSetManager.MetaDataAdd("VaildMovesPlayed", 1)
		moveID = self.DataSetManager.MoveIDLookUp.index(move)
		found, boardInfo = self.DataSetManager.GetBoardInfo(boardKey)
		
		with boardInfo.Lock:
			if found and moveID in boardInfo.Moves:
				if gameFinished:
					outComeKey = "GameFinished"
				else:
					outComeKey = BoardToKey(outComeBoard)
	
				move = boardInfo.Moves[moveID]
				boardInfo.BeingUsed = False
				if outComeKey in move.MoveOutComes:
					move.MoveOutComes[outComeKey] += 1
				else:
					move.MoveOutComes[outComeKey] = 1
				
		return

	def GameFinished(self, fitness):
		if not self.RecordMoves:
			return
		
		TempDataSetList = []

		for tempValue in self.TempDataSet.values():
			TempDataSetList += [tempValue]

		TempDataSetList.sort(key=GetSortKey, reverse=True)

		for tempValue in TempDataSetList:
			key = tempValue["BoardKey"]
			moveID = tempValue["MoveID"]

			found, boardInfo = self.DataSetManager.GetBoardInfo(key)
			if found:
				with boardInfo.Lock:
					if moveID in boardInfo.Moves:
						newFitness = boardInfo.Moves[moveID].AvgFitness*boardInfo.Moves[moveID].TimesPlayed
						newFitness += fitness
						boardInfo.Moves[moveID].TimesPlayed += 1
						newFitness /= boardInfo.Moves[moveID].TimesPlayed
						boardInfo.Moves[moveID].AvgFitness = newFitness

						if newFitness > boardInfo.BestAvgFitness:
							boardInfo.MoveIDOfBestAvgFitness = moveID
							boardInfo.BestAvgFitness = newFitness

						if not boardInfo.Finished:
							boardInfo.Finished = self.IsBoardFinished(boardInfo)
							if boardInfo.Finished:
								self.DataSetManager.MetaDataAdd("NumberOfFinishedBoards", 1)


		self.TempDataSet = {}
		self.InvalidMoveList = {}
		self.MoveNumber = 0
		return

	def TournamentFinished(self):
		
		return

	def IsBoardFinished(self, boardInfo):
		if boardInfo.Finished:
			return True

		if boardInfo.PlayedMovesLookUpArray < self.AllMovesPlayedValue:
			return False
		
		for moveId in range(self.DataSetManager.MaxMoveIDs):
			if moveId in boardInfo.Moves:
				if not self.IsMoveFinished(boardInfo, moveId):
					return False
						
		
		return True

	def IsMoveFinished(self, boardInfo, moveId):
		if boardInfo.Finished:
			return True

		if not (2**moveId & boardInfo.PlayedMovesLookUpArray):
			return False

		if moveId in boardInfo.Moves:

			for outComeKey in boardInfo.Moves[moveId].MoveOutComes:

				if outComeKey != "GameFinished":
					found, outComeBoardInfo = self.DataSetManager.GetBoardInfo(outComeKey)
					if not found:
						return False
					
					if not outComeBoardInfo.Finished:
						return False
			
		return True		

	def IsMoveLocked(self, boardInfo, moveId):
		if not (2**moveId & boardInfo.PlayedMovesLookUpArray):
			return False

		if moveId in boardInfo.Moves:

			for outComeKey in boardInfo.Moves[moveId].MoveOutComes:

				if outComeKey != "GameFinished":
					found, outComeBoardInfo = self.DataSetManager.GetBoardInfo(outComeKey)
					if not found:
						return False
					
					if outComeBoardInfo.BeingUsed or outComeBoardInfo.Lock.locked():
						return True
			
		return False		

	def AgentInfoOutput(self):
		info = ""
		info += "Base Agent test"
		#Todo add invalids per move 
		#add invalids per game
		#the point of these is to see if the agents are getting better or only the dataset
		total = sum(self.InvalidMoveList.values())
		
		info += "Invalids This Game: "+str(total)
		info += "\n"
		if len(self.InvalidMoveList) > 0:
			info += "Avg Invalids Per move: "+str(round(total/len(self.InvalidMoveList)))

		return info

def GetSortKey(val):
	return val["MoveNumber"]
