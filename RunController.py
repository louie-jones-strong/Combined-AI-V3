import RenderEngine.RenderEngine2D as RenderEngine
import Agents.BruteForceAgent as BruteForceAgent
import Agents.HumanAgent as HumanAgent
import DataManger.DataSetManager as DataSetManager
from Shared import OutputFormating as Format
from Shared import Logger
import importlib
import time
import os
import sys
os.system("cls")

def MakeAgentMove(turn, startBoard, AIs, game):
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

class RunController:

	Version = 1.1


	def __init__(self, simNumber=None, loadData=None, aiType=None, renderQuality=None, trainNetwork=None):
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

		if userInput == "N" or userInput == "n":
			self.RenderQuality = 0
			if trainNetwork == None:
				userInput = input("Train Network[Y/N]: ")
			else:
				userInput = trainNetwork

			import Agents.NeuralNetworkAgent as NeuralNetwork
			trainingMode = userInput == "Y" or userInput == "y"
			Ais = [NeuralNetwork.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode, trainingMode=trainingMode)]
		
			for loop in range(self.NumberOfBots-1):
				Ais += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]
		else:
			Ais = []
			for loop in range(self.NumberOfBots):
				Ais += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]

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
		if "SimulationBase.py" in files:
			files.remove("SimulationBase.py")


		for loop in range(len(files)):
			files[loop] = files[loop][:-3]
			if len(files) > 1 and simNumber == None:
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
			if self.AiDataManager.MetaData["Version"] == self.Version:
				os.system("cls")
				print("")
				print("SizeOfDataSet: "+str(self.AiDataManager.MetaData["SizeOfDataSet"]))
				print("NumberOfCompleteBoards: "+str(self.AiDataManager.MetaData["NumberOfCompleteBoards"]))
				print("NumberOfFinishedBoards: "+str(self.AiDataManager.MetaData["NumberOfFinishedBoards"]))
				print("NumberOfGames: "+str(self.AiDataManager.MetaData["NumberOfGames"]))
				print("TotalTime: "+Format.SplitTime(self.AiDataManager.MetaData["TotalTime"], roundTo=2))
				print("LastBackUpTotalTime: "+Format.SplitTime(self.AiDataManager.MetaData["LastBackUpTotalTime"], roundTo=2))
				print("")

				if loadData == None:
					userInput = input("load Dataset[Y/N]:")
				else:
					userInput = loadData
			else:
				print("MetaData Version "+str(self.AiDataManager.MetaData["Version"])+" != AiVersion "+str(self.Version)+" !")
				input()

		if userInput == "n" or userInput == "N":
			self.AiDataManager.MetaData = {}
			self.AiDataManager.MetaData["Version"] = self.Version
			self.AiDataManager.MetaData["SizeOfDataSet"] = 0
			self.AiDataManager.MetaData["NumberOfTables"] = 0
			self.AiDataManager.MetaData["FillingTable"] = 0
			self.AiDataManager.MetaData["NumberOfCompleteBoards"] = 0
			self.AiDataManager.MetaData["NumberOfFinishedBoards"] = 0
			self.AiDataManager.MetaData["NumberOfGames"] = 0
			self.AiDataManager.MetaData["NetworkUsingOneHotEncoding"] = False
			self.AiDataManager.MetaData["TotalTime"] = 0
			self.AiDataManager.MetaData["BruteForceTotalTime"] = 0
			self.AiDataManager.MetaData["AnnTotalTime"] = 0
			self.AiDataManager.MetaData["AnnDataMadeFromBruteForceTotalTime"] = 0
			self.AiDataManager.MetaData["LastBackUpTotalTime"] = 0
			self.AiDataManager.MetaData["AnnMoveInputShape"] = None
			self.AiDataManager.MetaData["AnnMoveStructreArray"] = None
			return False
		
		return True

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
			print("Number Of Finished Boards: " + str(Format.SplitNumber(self.AiDataManager.MetaData["NumberOfFinishedBoards"])))
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
			title += " CachingInfo: " + self.AiDataManager.GetLoadedDataInfo()
			title += " LastSaveTook: " + Format.SplitTime(self.LastSaveTook, roundTo=2)
			os.system("title "+title)
			self.LastOutputTime = time.time()

		elif self.RenderQuality == 1:
			self.RenderBoard(game, board)


		return
	
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
			board, turn, finished, fit = MakeAgentMove(turn, board, Ais, game)

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

					self.AiDataManager.Save()
					self.LastSaveTime = time.time()
					self.LastSaveTook = time.time() - self.LastSaveTook

				self.Output(game, numMoves, gameStartTime, board, turn, finished=True)

				board, turn = game.Start()
				numMoves = 0
				gameStartTime = time.time()
		return

if __name__ == "__main__":
	try:
		RunController(simNumber=None, loadData=None, aiType=None, renderQuality=0)
		RunController()

	except Exception as error:
		Logger.LogError(error)

