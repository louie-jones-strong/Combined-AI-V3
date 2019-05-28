import random
import sys
import DataManger.BoardInfo as BoardInfo
import Agents.AgentBase as AgentBase


class Agent(AgentBase.AgentBase):

	def __init__(self, dataSetManager, winningModeON=False):
		super().__init__(dataSetManager, winningModeON)

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
				if boardInfo.NumOfTriedMoves < self.DataSetManager.MaxMoveIDs:
					moveID = boardInfo.NumOfTriedMoves
					boardInfo.Moves[moveID] = BoardInfo.MoveInfo()
					boardInfo.NumOfTriedMoves += 1

					if boardInfo.NumOfTriedMoves >= self.DataSetManager.MaxMoveIDs:
						self.DataSetManager.MetaData["NumberOfCompleteBoards"] += 1

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

		if found and moveID in boardInfo.Moves:
			del boardInfo.Moves[moveID]

		if str(key)+str(moveID) in self.TempDataSet:
			del self.TempDataSet[str(key)+str(moveID)]
		return
	
	def UpdateMoveOutCome(self, board, move, outComeBoard, gameFinished=False):
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
