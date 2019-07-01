import random
import sys
import DataManger.BoardInfo as BoardInfo
import Agents.AgentBase as AgentBase
from DataManger.Serializer import BoardToKey

class Agent(AgentBase.AgentBase):

	def MoveCal(self, board):
		key = BoardToKey(board)
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
				if boardInfo.PlayedMovesLookUpArray < self.AllMovesPlayedValue:

					for moveID in range(self.DataSetManager.MaxMoveIDs):
						if not (2**moveID & boardInfo.PlayedMovesLookUpArray):
							break

				else:#played every move once already
					#nonFinishedLeastPlayed = sys.maxsize
					#nonFinishedMoveID = -1

					finishedLeastPlayed = sys.maxsize
					finishedMoveID = 0

					for movekey, moveValue in boardInfo.Moves.items():
						
						#if (not boardInfo.Finished) and moveValue.TimesPlayed < nonFinishedLeastPlayed:# and not self.IsMoveFinished(boardInfo, movekey):
						#	nonFinishedLeastPlayed = moveValue.TimesPlayed
						#	nonFinishedMoveID = movekey

						if moveValue.TimesPlayed < finishedLeastPlayed:
							finishedLeastPlayed = moveValue.TimesPlayed
							finishedMoveID = movekey
							
							if finishedLeastPlayed == 1:
								break

					#if nonFinishedMoveID != -1:
					#	moveID = nonFinishedMoveID
					#else:
					moveID = finishedMoveID

			else:#never played board before
				moveID = 0

		move = self.DataSetManager.MoveIDLookUp[moveID]
		self.RecordMove(board, move)
		return move
