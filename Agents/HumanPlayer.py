import random
import sys
import DataManger.BoardInfo as BoardInfo


class Agent(object):

	def __init__(self, dataSetManager, winningModeON=False):
		self.DataSetManager = dataSetManager
		
		return

	def MoveCal(self, board):
		numOfOutputs = self.DataSetManager.NumOfOutputs
		resolution = self.DataSetManager.OutputResolution
		minOutputSize = self.DataSetManager.MinOutputSize
		maxOutputSize = self.DataSetManager.MaxOutputSize

		move = []
		for loop in range(numOfOutputs):
			validMove = False
			while not validMove:
				userInput = float(input("input[" + str(loop) + "]: "))
				userInput = resolution * round(float(userInput)/resolution)
				print(userInput)
				if userInput >= minOutputSize and userInput <= maxOutputSize:
					validMove = True
					move += [userInput]
				else:
					print("not in the range!")
		return move

	def UpdateInvalidMove(self, board, move):
		return

	def UpdateMoveOutCome(self, board, move, outComeBoard, gameFinished=False):
		return

	def SaveData(self, fitness):
		return

