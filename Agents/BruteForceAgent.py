import random
import sys
import DataManger.BoardInfo as BoardInfo
import Agents.AgentBase as AgentBase


class Agent(AgentBase.AgentBase):

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

				else:#played every move once already
					leastPlayed = sys.maxsize
					moveID = 0
					for movekey, moveValue in boardInfo.Moves.items():
						
						if moveValue.TimesPlayed < leastPlayed:
							leastPlayed = moveValue.TimesPlayed
							moveID = movekey

			else:#never played board before
				moveID = 0

		move = self.DataSetManager.MoveIDLookUp[moveID]
		self.RecordMove(board, move)
		return move

