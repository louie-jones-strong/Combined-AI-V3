import random
import sys
import DataManger.BoardInfo as BoardInfo
import Agents.AgentBase as AgentBase
from DataManger.Serializer import BoardToKey

class Agent(AgentBase.AgentBase):
	MovesNotPlayedCache = {}
	AgentType = "BruteForce"

	def MoveCal(self, board):
		key = BoardToKey(board)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		moveID = None

		if self.WinningModeON:
			print("winnning mode!")
			if found and len(boardInfo.Moves) > 0:
				moveID = boardInfo.MoveIDOfBestAvgFitness

			else:#never played board before
				moveID = random.randint(0,self.DataSetManager.MaxMoveIDs-1)
				print("new Board!")


		else:  # learning mode
			if found:
				with boardInfo.Lock:
					if boardInfo.PlayedMovesLookUpArray < self.AllMovesPlayedValue:
						if key in self.MovesNotPlayedCache:
							moveID = self.MovesNotPlayedCache[key][0]
							del self.MovesNotPlayedCache[key][0]
	
							if len(self.MovesNotPlayedCache[key]) == 0:
								del self.MovesNotPlayedCache[key]
	
	
						else:
							notPlayedList = []
							for moveId in range(self.DataSetManager.MaxMoveIDs):
								if not (2**moveId & boardInfo.PlayedMovesLookUpArray):
									if moveID == None:
										moveID = moveId
									else:
										notPlayedList += [moveId]
	
							self.MovesNotPlayedCache[key] = notPlayedList
	
					else:#played every move once already
						nonFinishedLeastPlayed = sys.maxsize
						nonFinishedMoveID = -1
	
						finishedLeastPlayed = sys.maxsize
						finishedMoveID = 0
						foundNoneLockedBoard = False
	
						for movekey, moveValue in boardInfo.Moves.items():
							
							if (not boardInfo.Finished) and not self.IsMoveFinished(boardInfo, movekey) and moveValue.TimesPlayed < nonFinishedLeastPlayed:
								nonFinishedLeastPlayed = moveValue.TimesPlayed
								nonFinishedMoveID = movekey
	
							elif moveValue.TimesPlayed < finishedLeastPlayed:
								if not (foundNoneLockedBoard and self.IsMoveLocked(boardInfo, movekey)):
									foundNoneLockedBoard = True
									finishedLeastPlayed = moveValue.TimesPlayed
									finishedMoveID = movekey
									
									if finishedLeastPlayed == 1:
										break
	
						if nonFinishedMoveID != -1:
							moveID = nonFinishedMoveID
						else:
							moveID = finishedMoveID

			else:#never played board before
				moveID = 0

		move = self.DataSetManager.MoveIDLookUp[moveID]
		self.RecordMove(board, move)
		return move

	def MoveListCal(self, board):
		key = BoardToKey(board)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		moves = []

		if found:
			with boardInfo.Lock:
				if boardInfo.PlayedMovesLookUpArray < self.AllMovesPlayedValue:
					for moveId in range(self.DataSetManager.MaxMoveIDs):
						if not (2**moveId & boardInfo.PlayedMovesLookUpArray):
							moves += [self.DataSetManager.MoveIDLookUp[moveId]]
				else:
					for movekey, moveValue in boardInfo.Moves.items():
						moves += [self.DataSetManager.MoveIDLookUp[movekey]]


		else:#never played board before
			for moveId in range(self.DataSetManager.MaxMoveIDs):
				moves += [self.DataSetManager.MoveIDLookUp[moveId]]

		return moves

	def GameFinished(self, fitness):
		if len(self.MovesNotPlayedCache) >= 1000:
			self.MovesNotPlayedCache = {}

		super().GameFinished(fitness)
		return
