#%% imports
import Agents.BruteForceAgent as BruteForceAgent
import Agents.RandomAgent as RandomAgent
import Agents.HumanAgent as HumanAgent
import DataManger.DataSetManager as DataSetManager
from DataManger.Serializer import BoardToKey
from Shared import OutputFormating as Format
from Shared import Logger
from Shared.OSCalls import *
import importlib
import time
import os
import sys
import threading
ClearShell()
#%% setup

def MakeAgentMove(turn, board, agents, game):
	startBoardKey = BoardToKey(board)

	moveCalTime = 0
	makeMoveTime = 0
	updateInvalidMoveTime = 0
	checkFinishedTime = 0
	updateMoveOutComeTime = 0

	agent = agents[turn-1]
	valid = False
	#if turn == 1:
	while not valid:
		timeMark = time.time()
		move = agent.MoveCal(board)
		moveCalTime += time.time()-timeMark
		timeMark = time.time()
		valid, outComeBoard, turn = game.MakeMove(move)
		makeMoveTime += time.time()-timeMark
		if not valid:
			timeMark = time.time()
			agent.UpdateInvalidMove(board, move)
			updateInvalidMoveTime += time.time()-timeMark
	#else:
	#	board = game.FlipBoard(board)
	#	while not valid:
	#		timeMark = time.time()
	#		move = agent.MoveCal(board)
	#		moveCalTime += time.time()-timeMark
	#		flippedMove = game.FlipInput(move)
	#		
	#		timeMark = time.time()
	#		valid, outComeBoard, turn = game.MakeMove(flippedMove)
	#		makeMoveTime += time.time()-timeMark
	#		if not valid:
	#			timeMark = time.time()
	#			agent.UpdateInvalidMove(board, move)
	#			updateInvalidMoveTime += time.time()-timeMark

	timeMark = time.time()
	finished, fit = game.CheckFinished()
	checkFinishedTime += time.time()-timeMark

	timeMark = time.time()
	agent.UpdateMoveOutCome(startBoardKey, move, outComeBoard, finished)
	updateMoveOutComeTime += time.time()-timeMark

	#totalTime = moveCalTime+makeMoveTime+updateInvalidMoveTime+checkFinishedTime+updateMoveOutComeTime

	#print("AI  MoveCal Time:           "+str(moveCalTime))
	#print("Sim MakeMove Time:          "+str(makeMoveTime))
	#print("AI  UpdateInvalidMove Time: "+str(updateInvalidMoveTime))
	#print("Sim CheckFinished Time:     "+str(checkFinishedTime))
	#print("AI  UpdateMoveOutCome Time: "+str(updateMoveOutComeTime))
	#print("total Time: "+str(totalTime))
	return outComeBoard, turn, finished, fit

class RunController:

	Version = 1.2

	def __init__(self, simNumber=None, loadData=None, aiType=None, renderQuality=None, trainNetwork=None, stopTime=None):
		self.PickSimulation(simNumber)
		self.StopTime = stopTime

		#setting
		self.NumberOfBots = self.SimInfo["MaxPlayers"]
		self.LastOutputTime = time.time()
		self.LastSaveTook = 0
		self.WinningMode = False
		self.Agents = []

		if self.SimInfo["RenderSetup"]:
			self.RenderQuality = 1
		else:
			self.RenderQuality = 0

		self.AiDataManager = DataSetManager.DataSetManager(self.SimInfo["NumInputs"], self.SimInfo["MinInputSize"],
                                                     self.SimInfo["MaxInputSize"], self.SimInfo["Resolution"], self.SimInfo["SimName"])

		if aiType == None:
			userInput = input("Brute b) Network n) Random n) See Tree T) Human H):")
		else:
			userInput = aiType



		if userInput == "T" or userInput == "t":
			loadData = self.SetUpMetaData("Y")
			if loadData:
				import RenderEngine.TreeVisualiser as TreeVisualiser
				TreeVisualiser.TreeVisualiser(self.AiDataManager)

			input("hold here error!!!!!")


		else:
			loadData = self.SetUpMetaData(loadData)

			if userInput == "H" or userInput == "h":
				self.WinningMode = True
				self.Agents += [HumanAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]

				for loop in range(self.NumberOfBots-1):
					self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]


			elif userInput == "R" or userInput == "r":
				self.Agents += [RandomAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]

				for loop in range(self.NumberOfBots-1):
					self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]

			elif userInput == "N" or userInput == "n":
				if trainNetwork == None:
					userInput = input("Train Network[Y/N]: ")
				else:
					userInput = trainNetwork

				import Agents.NeuralNetworkAgent as NeuralNetwork
				trainingMode = userInput == "Y" or userInput == "y"
				self.Agents += [NeuralNetwork.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode, trainingMode=trainingMode)]

				for loop in range(self.NumberOfBots-1):
					self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]
			else:
				for loop in range(self.NumberOfBots):
					self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]

		if renderQuality != None:
			self.RenderQuality = renderQuality

		if self.RenderQuality == 2:
			import RenderEngine.RenderEngine2D as RenderEngine
			self.RenderEngine = RenderEngine.RenderEngine()
		return
	def PickSimulation(self, simNumber=None):
		files = os.listdir("Simulations")
		if "__pycache__" in files:
			files.remove("__pycache__")
		if "SimulationBase.py" in files:
			files.remove("SimulationBase.py")

		files = sorted(files)
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

		SetTitle("AI Playing:"+self.SimInfo["SimName"])

		return
	def SetUpMetaData(self, loadData=None):
		userInput = "N"

		if self.AiDataManager.GetMetaData():
			if self.AiDataManager.MetaData["Version"] == self.Version:
				if loadData == None:
					ClearShell()
					print("")
					print("SizeOfDataSet: "+str(self.AiDataManager.MetaData["SizeOfDataSet"]))
					print("NumberOfCompleteBoards: "+str(self.AiDataManager.MetaData["NumberOfCompleteBoards"]))
					print("NumberOfFinishedBoards: "+str(self.AiDataManager.MetaData["NumberOfFinishedBoards"]))
					print("NumberOfGames: "+str(self.AiDataManager.MetaData["NumberOfGames"]))
					print("TotalTime: "+Format.SplitTime(self.AiDataManager.MetaData["TotalTime"], roundTo=2))
					print("LastBackUpTotalTime: "+Format.SplitTime(self.AiDataManager.MetaData["LastBackUpTotalTime"], roundTo=2))
					print("")
					userInput = input("load Dataset[Y/N]:")
				else:
					userInput = loadData
			else:
				print("MetaData Version "+str(self.AiDataManager.MetaData["Version"])+" != AiVersion "+str(self.Version)+" !")
				input()

		if userInput == "n" or userInput == "N":
			self.AiDataManager.MetaData = {}
			self.AiDataManager.MetaDataSet("Version", self.Version)
			self.AiDataManager.MetaDataSet("SizeOfDataSet", 0)
			self.AiDataManager.MetaDataSet("NumberOfTables", 0)
			self.AiDataManager.MetaDataSet("FillingTable", 0)
			self.AiDataManager.MetaDataSet("NumberOfCompleteBoards", 0)
			self.AiDataManager.MetaDataSet("NumberOfFinishedBoards", 0)
			self.AiDataManager.MetaDataSet("NumberOfGames", 0)
			self.AiDataManager.MetaDataSet("NetworkUsingOneHotEncoding", False)
			self.AiDataManager.MetaDataSet("RealTime", 0)
			self.AiDataManager.MetaDataSet("TotalTime", 0)
			self.AiDataManager.MetaDataSet("BruteForceTotalTime", 0)
			self.AiDataManager.MetaDataSet("AnnTotalTime", 0)
			self.AiDataManager.MetaDataSet("AnnDataMadeFromBruteForceTotalTime", 0)
			self.AiDataManager.MetaDataSet("LastBackUpTotalTime", 0)
			self.AiDataManager.MetaDataSet("AnnMoveInputShape", None)
			self.AiDataManager.MetaDataSet("AnnMoveStructreArray", None)
			self.AiDataManager.MetaDataSet("AnnRunId", None)
			return False
		
		return True

	def RenderBoard(self, game, board):

		if self.RenderQuality == 1:
			game.SimpleBoardOutput(board)
		elif self.RenderQuality == 2:
			timeMark = time.time()
			self.RenderEngine.PieceList = game.ComplexBoardOutput(board)
			timeMark = time.time()-timeMark
			if not self.RenderEngine.UpdateWindow(timeMark):
				self.RenderQuality = 0


		return
	def Output(self, game, numMoves, gameStartTime, board, turn, finished=False):
		if self.RenderQuality == 0:
			return
		if (time.time() - self.LastOutputTime) >= 0.5 or self.WinningMode:
			numGames = self.AiDataManager.MetaData["NumberOfGames"]+1
			avgMoveTime = 0
			if numMoves != 0:
				avgMoveTime = (time.time() - gameStartTime)/numMoves
				avgMoveTime = round(avgMoveTime, 6)


			ClearShell()
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
			print("Games avg took: " + Format.SplitTime(totalTime/numGames, roundTo=6))
			print("time since start: " + Format.SplitTime(totalTime))
			print("Real Time since start: " + Format.SplitTime(self.AiDataManager.MetaData["RealTime"]))

			backUpTime = self.AiDataManager.MetaData["LastBackUpTotalTime"]
			print("time since last BackUp: " + Format.SplitTime(totalTime-backUpTime))
			print("press CTRl+Q to quit...")
			
			title = "AI Playing: "+self.SimInfo["SimName"]
			title += " Time Since Last Save: " + Format.SplitTime(time.time()-self.LastSaveTime, roundTo=1)
			title += " CachingInfo: " + self.AiDataManager.GetLoadedDataInfo()
			title += " LastSaveTook: " + Format.SplitTime(self.LastSaveTook)
			SetTitle(title)
			self.LastOutputTime = time.time()

		elif self.RenderQuality == 2:
			self.RenderBoard(game, board)


		return
	
	def RunTournament(self):
		targetThreadNum = 2

		threads = []
		for loop in range(targetThreadNum-1):
			game = self.Sim.CreateNew()
			agents = []
			for loop in range(self.NumberOfBots):
				agents += [BruteForceAgent.Agent(self.AiDataManager, False, winningModeON=self.WinningMode)]
			thread = threading.Thread(target=self.RunSimMatch, args=(game, agents, False,))
			threads += [thread]
			thread.start()


		self.RunSimMatch(self.Sim, self.Agents, True)
		for thread in threads:
			thread.join()

		self.SaveData()
		return

	def RunSimMatch(self, game, agents, isMainThread):
		board, turn = game.Start()
		self.AiDataManager.UpdateStartingBoards(board)

		numMoves = 0
		totalStartTime = time.time()
		gameStartTime = time.time()
		self.LastSaveTime = time.time()
		while True:
			if isMainThread:
				self.Output(game, numMoves, gameStartTime, board, turn)
			board, turn, finished, fit = MakeAgentMove(turn, board, agents, game)

			numMoves += 1
			temp = time.time()-totalStartTime
			self.AiDataManager.MetaDataAdd("TotalTime", temp)
			if isMainThread:
				self.AiDataManager.MetaDataAdd("RealTime", temp)
			totalStartTime = time.time()

			if finished:
				self.AiDataManager.MetaDataAdd("NumberOfGames", 1)

				for loop in range(len(agents)):
					agents[loop].SaveData(fit[loop])

				if isMainThread:
					self.Output(game, numMoves, gameStartTime, board, turn, finished=True)

					if time.time()-self.LastSaveTime > 60:
						self.SaveData()

				if self.StopTime != None and self.AiDataManager.MetaData["RealTime"] >= self.StopTime:
					break

				board, turn = game.Start()
				self.AiDataManager.UpdateStartingBoards(board)
				numMoves = 0
				gameStartTime = time.time()
		return

	def SaveData(self):
		self.LastSaveTook = time.time()
		# save back up every hour
		if self.AiDataManager.MetaData["TotalTime"]-self.AiDataManager.MetaData["LastBackUpTotalTime"] > 60*60:
			self.AiDataManager.BackUp()

		self.AiDataManager.Save()
		self.LastSaveTime = time.time()
		self.LastSaveTook = time.time() - self.LastSaveTook
		return


if __name__ == "__main__":
	hadError = False

	try:
		#controller = RunController(renderQuality=1)
		controller = RunController(simNumber=6, loadData="N", aiType="b", renderQuality=1)

	except Exception as error:
		Logger.LogError(error)
		hadError= True

#%%
	if not hadError:
		try:
			controller.RunTournament()

		except Exception as error:
			Logger.LogError(error)
