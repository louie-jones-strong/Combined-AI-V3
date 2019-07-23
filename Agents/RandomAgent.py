import random
import Agents.AgentBase as AgentBase
from DataManger.Serializer import BoardToKey

class Agent(AgentBase.AgentBase):

	def MoveCal(self, board):
		key = BoardToKey(board)
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)

		if found:
			with boardInfo.Lock:
				movesIds = []
				for moveId in range(self.DataSetManager.MaxMoveIDs):
				
					if not(2**moveId & boardInfo.PlayedMovesLookUpArray) or moveId in boardInfo.Moves:
						movesIds += [moveId]

			pickedIndex = random.randint(0,len(movesIds)-1)
			moveID = movesIds[pickedIndex]

		else:
			moveID = random.randint(0,self.DataSetManager.MaxMoveIDs-1)

		move = self.DataSetManager.MoveIDLookUp[moveID]
		self.RecordMove(board, move)
		return move

