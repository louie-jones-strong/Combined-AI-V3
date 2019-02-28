import BruteForce
import NeuralNetwork
import importlib
import time
import os
import sys
from threading import Thread
import keyboard

def MakeAIMove(turn, board, AIs, game):
	AI = AIs[turn-1]
	valid = False
	if turn == 1:
		while not valid:
			flippedBoard = game.FlipBoard(board)
			move = AI.MoveCal(flippedBoard)		
			flippedMove = game.FlipInput(move)
			valid, board, turn = game.MakeMove(flippedMove)

			if not valid:
				AI.UpdateInvalidMove(flippedBoard, move)
	else:
		while not valid:
			move = AI.MoveCal(board)
			valid, board, turn = game.MakeMove(move)
			if not valid:
				AI.UpdateInvalidMove(board, move)

	return board, turn

def SaveMetaData(metaData, address):
	file = open(address, "w")
	for key, value in metaData.items():
		file.write(str(key)+":"+str(value)+"\n")
	file.close() 
	return
def LoadMetaData(address):
	metaData = {}

	file = open(address, "r")
	lines = file.readlines()
	file.close() 
	for loop in range(len(lines)):
		line = lines[loop][:-1]
		line = line.split(":")
		key = line[0]
		value = line[1]
		if "." in value:
			value = float(value)
		else:
			value = int(value)
		metaData[key] = value
	

	return metaData

def SplitNumber(number):
	output = ""
	number = str(number)
	lenght = len(number)
	if lenght < 4:
		output += str(number)
	else:
		start = lenght % 3
		if start > 0:
			output += str(number[:start]) + ","
		gap = 0
		for loop in range(start, lenght):
			output += str(number[loop])
			gap += 1
			if gap == 3 and loop < lenght-1:
				output += ","
				gap = 0
	return output
def SplitTime(seconds, roundTo=0):
	#Convert seconds to string "[[[DD:]HH:]MM:]SS"
	output = ""
	for scale in 86400, 3600, 60:
		result, seconds = divmod(seconds, scale)
		if output != "" or result > 0:
			if output != "":
				output += ":"
			output += str(int(result))
	if output != "":
		output += ":"
	output += str(round(seconds, roundTo))
	return output

class RunController(object):
	def PickSimulation(self):
		files = os.listdir("Simulations")
		if "__pycache__" in files:
			files.remove("__pycache__")
		if "SimulationInterface.py" in files:
			files.remove("SimulationInterface.py")
		for loop in range(len(files)):
			files[loop] = files[loop][:-3]
			if len(files) > 1:
				print(str(loop+1)+") " + files[loop])
		userInput = 1
		if len(files) > 1:
			userInput = int(input("pick Simulation: "))
		if userInput > len(files):
			userInput = len(files)
		if userInput < 1:
			userInput = 1
		simName = files[userInput-1]

		os.system("title "+"AI Playing:"+simName)
		self.Sim = importlib.import_module("Simulations." + simName)
		self.SimInfo = self.Sim.Simulation().Info

		return simName
	def SetUpMetaData(self):
		userInput = "N"

		if os.path.isfile(self.DatasetAddress+"MetaData.txt"):
			self.MetaData = LoadMetaData(self.DatasetAddress+"MetaData.txt")
			print("")
			print("SizeOfDataSet: "+str(self.MetaData["SizeOfDataSet"]))
			print("NumberOfCompleteBoards: "+str(self.MetaData["NumberOfCompleteBoards"]))
			print("NumberOfGames: "+str(self.MetaData["NumberOfGames"]))
			print("TotalTime: "+SplitTime(self.MetaData["TotalTime"], roundTo=2))
			print("")

			userInput = input("load Dataset[Y/N]:")

		if userInput == "n" or userInput == "N":
			self.MetaData = {"SizeOfDataSet":0, "NumberOfCompleteBoards": 0, "NumberOfGames": 0, "TotalTime": 0}
			return False
		else:
			self.AiDataManager.NumberOfCompleteBoards = self.MetaData["NumberOfCompleteBoards"]
			return True

		return False

	def __init__(self):
		simName = self.PickSimulation()

		#setup dataset address
		temp = "DataSets//"+simName
		if not os.path.exists(temp):
			os.makedirs(temp)
		self.DatasetAddress = temp+"//"+simName

		#setting
		self.NumberOfBots = self.SimInfo["MaxPlayers"]
		self.LastOutputTime = time.time()
		self.WinningMode = False

		if self.NumberOfBots >= 1:
			userInput = input("Human Player[Y/N]:")
			if userInput == "y" or userInput == "Y":
				self.WinningMode = True
				self.NumberOfBots -= 1

		self.AiDataManager = BruteForce.DataSetManager( self.SimInfo["NumInputs"], self.SimInfo["MinInputSize"], 
														self.SimInfo["MaxInputSize"], self.SimInfo["Resolution"], self.DatasetAddress)

		loadData = self.SetUpMetaData()
		if loadData:
			self.AiDataManager.LoadDataSet()

		userInput = input("Brute b) network n):")
		if userInput == "N" or userInput == "n":
			Ais = [NeuralNetwork.NeuralNetwork(self.SimInfo["NumInputs"], self.SimInfo["MinInputSize"], 
												self.SimInfo["MaxInputSize"], self.SimInfo["Resolution"], self.DatasetAddress)]
			Ais[0].LoadData()

			for loop in range(self.NumberOfBots-1):
				Ais += [BruteForce.BruteForce(self.AiDataManager, winningModeON=self.WinningMode)]
		else:
			Ais = []
			for loop in range(self.NumberOfBots):
				Ais += [BruteForce.BruteForce(self.AiDataManager, winningModeON=self.WinningMode)]

		self.RunTournament(Ais)
		return

	def Output(self, game, numMoves, gameStartTime, board, turn, finished=False):
		if (time.time() - self.LastOutputTime) >= 0.5:
			numGames = self.MetaData["NumberOfGames"]+1
			avgMoveTime = 0
			if numMoves != 0:
				avgMoveTime = (time.time() - gameStartTime)/numMoves
				avgMoveTime = round(avgMoveTime, 6)


			os.system("cls")
			if self.NumberOfBots >= turn:
				game.SimpleOutput(board)

			print("Dataset size: " + str(SplitNumber(len(self.AiDataManager.DataSet))))
			print("Number Of Complete Boards: " + str(SplitNumber(self.AiDataManager.NumberOfCompleteBoards)))
			if finished:
				print("game: " + str(SplitNumber(numGames)) + " move: " + str(SplitNumber(numMoves)) + " finished game")
			else:
				print("game: " + str(SplitNumber(numGames)) + " move: " + str(SplitNumber(numMoves)))
			print("moves avg took: " + str(avgMoveTime) + " seconds")
			totalTime = self.MetaData["TotalTime"]
			print("Games avg took: " + str(SplitTime(totalTime/numGames, roundTo=6)))
			print("time since start: " + str(SplitTime(totalTime, roundTo=2)))
			print("press CTRl+Q to quit...")
			
			self.LastOutputTime = time.time()
		return
	
	def MakeHumanMove(self, game, board):
		valid = False
		while not valid:
			os.system("cls")
			game.SimpleOutput(board)
			move = []
			for loop in range(self.SimInfo["NumInputs"]):
				validMove = False
				while not validMove:
					userInput = float(input("input["+ str(loop) +"]: "))
					userInput = self.SimInfo["Resolution"] * round(float(userInput)/self.SimInfo["Resolution"])
					print(userInput)
					if userInput >= self.SimInfo["MinInputSize"] and userInput <= self.SimInfo["MaxInputSize"]:
						validMove = True
						move += [userInput]
					else:
						print("not in the range!")
			valid, board, turn = game.MakeMove(move)
			if not valid:
				print("that move was not vaild")
					
		print("")
		game.SimpleOutput(board)
		return board, turn

	def RunTournament(self, Ais):
		self.RunSimMatch(Ais)
		return

	def RunSimMatch(self, Ais):
		game = self.Sim.Simulation()
		board, turn = game.Start()

		numMoves = 0
		totalStartTime = time.time()
		gameStartTime = time.time()
		lastSaveTime = time.time()
		while True:
			if self.NumberOfBots >= turn:
				board, turn = MakeAIMove(turn, board, Ais, game)
			else:
				board, turn = self.MakeHumanMove(game, board)

			numMoves += 1
			self.MetaData["TotalTime"] += time.time()-totalStartTime
			totalStartTime = time.time()
			self.Output(game, numMoves, gameStartTime, board, turn)

			finished, fit = game.CheckFinished()
			
			if keyboard.is_pressed("CTRl+Q"):
				break

			if finished:
				if time.time() - lastSaveTime > 10:
					for loop in range(len(Ais)):
						Ais[loop].SaveData(fit[loop])

					self.MetaData["NumberOfCompleteBoards"] = self.AiDataManager.NumberOfCompleteBoards
					self.MetaData["SizeOfDataSet"] = len(self.AiDataManager.DataSet)
					SaveMetaData(self.MetaData, self.DatasetAddress+"MetaData.txt")
					lastSaveTime = time.time()

				if keyboard.is_pressed("CTRl+Q"):
					break

				self.Output(game, numMoves, gameStartTime, board, turn, finished=True)

				board, turn = game.Start()
				self.MetaData["NumberOfGames"] += 1
				numMoves = 0
				gameStartTime = time.time()
		return

if __name__ == "__main__":
	RunController()
