import BruteForce
import NeuralNetwork
import importlib
import time
import os
import sys
from threading import Thread
import keyboard

def MakeAIMove(turn, board, AIs, game):
	time1 = 0
	time2 = 0
	time3 = 0
	time4 = 0

	AI = AIs[turn-1]
	valid = False
	if turn == 1:
		while not valid:
			mark = time.time()
			flippedBoard = game.FlipBoard(board)
			time1 += time.time()-mark

			mark = time.time()
			move = AI.MoveCal(flippedBoard)
			time2 += time.time()-mark
			
			flippedMove = game.FlipInput(move)

			mark = time.time()
			valid, board, turn = game.MakeMove(flippedMove)
			time3 += time.time()-mark

			if not valid:
				mark = time.time()
				AI.UpdateInvalidMove(flippedBoard, move)
				time4 += time.time()-mark
		#print("time1: "+str(time1))
		#print("time2: "+str(time2))
		#print("time3: "+str(time3))
		#print("time4: "+str(time4))
		#input("next: ")
		#0.08
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

		if os.path.isfile(self.MetaDataAddress):
			self.MetaData = LoadMetaData(self.MetaDataAddress)
			print("")
			print("SizeOfDataSet: "+str(self.MetaData["SizeOfDataSet"]))
			print("NumberOfCompleteBoards: "+str(self.MetaData["NumberOfCompleteBoards"]))
			print("NumberOfGames: "+str(self.MetaData["NumberOfGames"]))
			print("TotalTime: "+SplitTime(self.MetaData["TotalTime"], roundTo=2))
			print("")

			userInput = input("load Dataset[Y/N]:")

		if userInput == "n" or userInput == "N":
			self.MetaData = {"SizeOfDataSet":0, "NumberOfCompleteBoards": 0, "NumberOfGames": 0, "TotalTime": 0}
		else:
			self.AiDataManager.LoadDataSet()
			self.AiDataManager.NumberOfCompleteBoards = self.MetaData["NumberOfCompleteBoards"]

		return

	def __init__(self):
		simName = self.PickSimulation()

		#setup dataset address
		temp = "DataSets//"+simName
		if not os.path.exists(temp):
			os.makedirs(temp)
		self.MetaDataAddress = temp+"//"+simName+"MetaData.txt"
		self.DatasetAddress = temp+"//"+simName+"Dataset"

		#setting
		self.RenderQuality = int(input("Render level[0][1][2]: "))
		self.NumberOfBots = self.SimInfo["MaxPlayers"]
		self.LastOutputTime = time.time()

		if self.RenderQuality != 0:
			userInput = input("Human Player[Y/N]:")
			if userInput == "y" or userInput == "Y":
				self.NumberOfBots -= 1

		self.AiDataManager = BruteForce.DataSetManager( self.SimInfo["NumInputs"], self.SimInfo["MinInputSize"], 
														self.SimInfo["MaxInputSize"], self.SimInfo["Resolution"], self.DatasetAddress)

		Test(self.AiDataManager)
		self.SetUpMetaData()

		self.WinningMode = False
		if self.NumberOfBots == 1:
			self.WinningMode = True

		if self.RenderQuality == 2:
			import RenderEngine
			self.RenderEngine = RenderEngine.RenderEngine()

		#Thread(target=self.NetworkTrain).start()
		self.BruteForceRun()
		return

	def Output(self, game, numMoves, gameStartTime, board, turn, finished=False):
		numGames = self.MetaData["NumberOfGames"]+1
		avgMoveTime = 0
		if numMoves != 0:
			avgMoveTime = (time.time() - gameStartTime)/numMoves
			avgMoveTime = round(avgMoveTime,6)
		
		if self.RenderQuality == 2:
			text = "Dataset Size: "+str(len(self.AiDataManager.DataSet))+"\n"
			text += "Game: "+str(numGames)+"\n"
			text += "Move: "+str(numMoves)+"\n"
			text += "AVG time: "+str(avgMoveTime)
			self.RenderEngine.UpdateConsoleText(text)

			if board != None and turn != None:
				self.RenderEngine.UpdateBoard(board, turn)
			self.RenderEngine.UpdateFrame()

		if (time.time() - self.LastOutputTime) >= 1:
			if self.RenderQuality == 1 and self.NumberOfBots >= turn:
				os.system("cls")
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
		if self.RenderQuality == 1:

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
		
		elif self.RenderQuality == 2:
			board, turn = self.RenderEngine.MakeHumanMove(game)
		return board, turn

	def BruteForceRun(self):
		game = self.Sim.Simulation()
		AIs = []
		for loop in range(2):
			AIs += [BruteForce.BruteForce(self.AiDataManager, winningModeON=self.WinningMode)]
		board, turn = game.Start()

		numMoves = 0

		totalStartTime = time.time()
		gameStartTime = time.time()
		lastSaveTime = time.time()
		while True:
			if self.NumberOfBots >= turn:
				board, turn = MakeAIMove(turn, board, AIs, game)
			else:
				board, turn = self.MakeHumanMove(game, board)

			numMoves += 1
			self.MetaData["TotalTime"] += time.time()-totalStartTime
			totalStartTime = time.time()
			self.Output(game, numMoves, gameStartTime, board, turn)

			finished, fit = game.CheckFinished()
			if finished:
				if time.time() - lastSaveTime > 5:
					for loop in range(len(AIs)):
						AIs[loop].UpdateData(fit[loop])

					self.MetaData["NumberOfCompleteBoards"] = self.AiDataManager.NumberOfCompleteBoards
					self.MetaData["SizeOfDataSet"] = len(self.AiDataManager.DataSet)
					SaveMetaData(self.MetaData, self.MetaDataAddress)
					lastSaveTime = time.time()

				if keyboard.is_pressed("CTRl+Q"):
					break

				self.Output(game, numMoves, gameStartTime, board, turn, finished=True)

				board, turn = game.Start()
				self.MetaData["NumberOfGames"] += 1
				numMoves = 0
				gameStartTime = time.time()
		return

	def NetworkTrain(self):
		Ai = NeuralNetwork.NeuralNetwork(self.DatasetAddress)
		while True:
			Ai.ImportDataSet()
			Ai.Train(20)

		return


def Test(AiDataManager):
	timeMark = time.time()
	AiDataManager.LoadDataSet()
	print("time taken to load: "+str(time.time()-timeMark))

	num = AiDataManager.SetupNewAI()
	timeMark = time.time()
	AiDataManager.SaveDataSet(num)
	print("time taken to save: "+str(time.time()-timeMark))

	input("testing finished: ")
	return

if __name__ == "__main__":
	RunController()
