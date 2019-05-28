import RenderEngine.RenderEngine2D as RenderEngine
import AIs.BruteForce as BruteForce
import DataManger.DataSetManager as DataSetManager
from Shared import OutputFormating as Format
import importlib
import time
import os
import sys

def MakeAIMove(turn, startBoard, AIs, game):
	startBoard = startBoard[:]  # copy to break references

	AI = AIs[turn-1]
	valid = False
	if turn == 1:
		startBoard = game.FlipBoard(startBoard)
		while not valid:
			move = AI.MoveCal(startBoard)
			flippedMove = game.FlipInput(move)

			valid, outComeBoard, turn = game.MakeMove(flippedMove)

			if not valid:
				AI.UpdateInvalidMove(startBoard, move)
	else:
		while not valid:
			move = AI.MoveCal(startBoard)

			valid, outComeBoard, turn = game.MakeMove(move)

			if not valid:
				AI.UpdateInvalidMove(startBoard, move)

	finished, fit = game.CheckFinished()

	AI.UpdateMoveOutCome(startBoard, move, outComeBoard, finished)

	return outComeBoard, turn, finished, fit

class RunController(object):
	def __init__(self, simNumber=None, loadData=None, aiType=None, renderQuality=None):
		self.PickSimulation(simNumber)

		#setting
		self.NumberOfBots = self.SimInfo["MaxPlayers"]
		self.LastOutputTime = time.time()
		self.LastSaveTook = 0
		self.WinningMode = False

		if self.SimInfo["RenderSetup"]:
			self.RenderQuality = 1
		else:
			self.RenderQuality = 0

		#if self.NumberOfBots >= 1:
		#	userInput = input("Human Player[Y/N]:")
		#	if userInput == "y" or userInput == "Y":
		#		self.WinningMode = True
		#		self.NumberOfBots -= 1

		self.AiDataManager = DataSetManager.DataSetManager(self.SimInfo["NumInputs"], self.SimInfo["MinInputSize"],
                                                     self.SimInfo["MaxInputSize"], self.SimInfo["Resolution"], self.SimInfo["SimName"])

		loadData = self.SetUpMetaData(loadData)
		if aiType == None:
			userInput = input("Brute b) network n):")
		else:
			userInput = aiType

		if loadData:
			if not self.AiDataManager.LoadDataSet():
				input("Failed To Load Data")

		if userInput == "N" or userInput == "n":
			self.RenderQuality = 0
			import AIs.NeuralNetwork as NeuralNetwork
			Ais = [NeuralNetwork.NeuralNetwork(
			    self.AiDataManager, winningModeON=self.WinningMode)]

			for loop in range(self.NumberOfBots-1):
				Ais += [BruteForce.BruteForce(self.AiDataManager,
				                              winningModeON=self.WinningMode)]
		else:
			Ais = []
			for loop in range(self.NumberOfBots):
				Ais += [BruteForce.BruteForce(self.AiDataManager,
				                              winningModeON=self.WinningMode)]

		if renderQuality != None:
			self.RenderQuality = renderQuality

		if self.RenderQuality == 1:
			self.RenderEngine = RenderEngine.RenderEngine()
		self.RunTournament(Ais)
		return
	def PickSimulation(self, simNumber=None):
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
			if simNumber == None:
				userInput = int(input("pick Simulation: "))
			else:
				userInput = simNumber

		if userInput > len(files):
			userInput = len(files)
		if userInput < 1:
			userInput = 1
		simName = files[userInput-1]

		self.Sim = importlib.import_module("Simulations." + simName)
		self.Sim = self.Sim.Simulation()
		self.SimInfo = self.Sim.Info

		os.system("title "+"AI Playing:"+self.SimInfo["SimName"])

		return
	def SetUpMetaData(self, loadData=None):
		userInput = "N"

		if self.AiDataManager.GetMetaData():
			os.system("cls")
			print("")
			print("SizeOfDataSet: "+str(self.AiDataManager.MetaData["SizeOfDataSet"]))
			print("NumberOfCompleteBoards: "+str(self.AiDataManager.MetaData["NumberOfCompleteBoards"]))
			print("NumberOfGames: "+str(self.AiDataManager.MetaData["NumberOfGames"]))
			print("TotalTime: "+Format.SplitTime(self.AiDataManager.MetaData["TotalTime"], roundTo=2))
			print("LastBackUpTotalTime: "+Format.SplitTime(self.AiDataManager.MetaData["LastBackUpTotalTime"], roundTo=2))
			print("")

			if loadData == None:
				userInput = input("load Dataset[Y/N]:")
			else:
				userInput = loadData

		if userInput == "n" or userInput == "N":
			self.AiDataManager.MetaData = {"SizeOfDataSet": 0,
                                  "NumberOfCompleteBoards": 0,
                                  "NumberOfGames": 0,
                                  "NetworkUsingOneHotEncoding": False,
                                  "TotalTime": 0,
                                  "BruteForceTotalTime": 0,
                                  "AnnTotalTime": 0,
                                  "AnnDataMadeFromBruteForceTotalTime": 0,
                                  "LastBackUpTotalTime": 0}
			return False
		else:
			return True

		return False

	def RenderBoard(self, game, board):

		if self.RenderQuality == 0:
			game.SimpleBoardOutput(board)
		else:
			timeMark = time.time()
			self.RenderEngine.PieceList = game.ComplexBoardOutput(board)
			timeMark = time.time()-timeMark
			if not self.RenderEngine.UpdateWindow(timeMark):
				self.RenderQuality = 0


		return
	def Output(self, game, numMoves, gameStartTime, board, turn, finished=False):

		if (time.time() - self.LastOutputTime) >= 0.5:
			numGames = self.AiDataManager.MetaData["NumberOfGames"]+1
			avgMoveTime = 0
			if numMoves != 0:
				avgMoveTime = (time.time() - gameStartTime)/numMoves
				avgMoveTime = round(avgMoveTime, 6)


			os.system("cls")
			self.RenderBoard(game, board)
			print("")
			print("Dataset size: " + str(Format.SplitNumber(self.AiDataManager.GetNumberOfBoards())))
			print("Number Of Complete Boards: " + str(Format.SplitNumber(self.AiDataManager.MetaData["NumberOfCompleteBoards"])))
			if finished:
				print("game: " + str(Format.SplitNumber(numGames)) + " move: " + str(Format.SplitNumber(numMoves)) + " finished game")
			else:
				print("game: " + str(Format.SplitNumber(numGames)) + " move: " + str(Format.SplitNumber(numMoves)))
			print("moves avg took: " + str(avgMoveTime) + " seconds")
			totalTime = self.AiDataManager.MetaData["TotalTime"]
			print("Games avg took: " + str(Format.SplitTime(totalTime/numGames, roundTo=6)))
			print("time since start: " + str(Format.SplitTime(totalTime, roundTo=2)))

			backUpTime = self.AiDataManager.MetaData["LastBackUpTotalTime"]
			print("time since last BackUp: " + str(Format.SplitTime(totalTime-backUpTime, roundTo=2)))
			print("press CTRl+Q to quit...")
			
			title = "AI Playing: "+self.SimInfo["SimName"]
			title += " Time Since Last Save: " + Format.SplitTime(time.time()-self.LastSaveTime, roundTo=1)
			title += " CachingInfo: " + self.AiDataManager.GetCachingInfoString()
			title += " LastSaveTook: " + Format.SplitTime(self.LastSaveTook, roundTo=2)
			os.system("title "+title)
			self.LastOutputTime = time.time()

		elif self.RenderQuality == 1:
			self.RenderBoard(game, board)


		return
	
	def MakeHumanMove(self, game, board):
		valid = False
		while not valid:
			os.system("cls")
			self.RenderBoard(game, board)
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

		finished, fit = game.CheckFinished()

		print("")
		self.RenderBoard(game, board)
		return board, turn, finished, fit

	def RunTournament(self, Ais):
		
		self.RunSimMatch(Ais, self.Sim)
		
		game = self.Sim.CreateNew()
		self.RunSimMatch(Ais, game)
		return

	def RunSimMatch(self, Ais, game):
		board, turn = game.Start()

		numMoves = 0
		totalStartTime = time.time()
		gameStartTime = time.time()
		self.LastSaveTime = time.time()
		while True:
			if self.NumberOfBots >= turn:
				board, turn, finished, fit = MakeAIMove(turn, board, Ais, game)
			else:
				board, turn, finished, fit = self.MakeHumanMove(game, board)

			numMoves += 1
			self.AiDataManager.MetaData["TotalTime"] += time.time()-totalStartTime
			totalStartTime = time.time()
			self.Output(game, numMoves, gameStartTime, board, turn)

			if finished:
				self.AiDataManager.MetaData["NumberOfGames"] += 1

				for loop in range(len(Ais)):
					Ais[loop].SaveData(fit[loop])

				if time.time() - self.LastSaveTime > 60:
					self.LastSaveTook = time.time()
					# save back up every hour
					if self.AiDataManager.MetaData["TotalTime"]-self.AiDataManager.MetaData["LastBackUpTotalTime"] > 60*60:
						self.AiDataManager.BackUp()

					self.AiDataManager.SaveDataSet()
					self.LastSaveTime = time.time()
					self.LastSaveTook = time.time() - self.LastSaveTook

				self.Output(game, numMoves, gameStartTime, board, turn, finished=True)

				board, turn = game.Start()
				numMoves = 0
				gameStartTime = time.time()
		return

if __name__ == "__main__":
	RunController(simNumber=6, loadData="Y", aiType=None, renderQuality=0)
	RunController()
