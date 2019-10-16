import Agents.BruteForceAgent as BruteForceAgent
import Agents.RandomAgent as RandomAgent
import Agents.HumanAgent as HumanAgent
import DataManger.DataSetManager as DataSetManager
from DataManger.Serializer import BoardToKey
from Shared import OutputFormating as Format
from Shared import Logger
import importlib
import time
import os
import sys
import threading


def MakeAgentMove(turn, board, agents, outcomePredictor, game):
	startBoardKey = BoardToKey(board)

	agent = agents[turn-1]
	valid = False
	while not valid:
		move = agent.MoveCal(board)
		
		outcomePredictor.PredictOutput(board, move)

		valid, outComeBoard, turn = game.MakeMove(move)

		if not valid:
			agent.UpdateInvalidMove(board, move)

			if outcomePredictor != None:
				outcomePredictor.UpdateInvalidMove(board, move)


	finished, fit = game.CheckFinished()

	if outcomePredictor != None:
		outcomePredictor.UpdateMoveOutCome(startBoardKey, move, outComeBoard, finished)

	agent.UpdateMoveOutCome(startBoardKey, move, outComeBoard, finished)

	return outComeBoard, turn, finished, fit

class RunController:

	Version = 1.5

	def __init__(self, logger, simNumber=None, loadData=None, aiType=None, renderQuality=None, trainNetwork=None, stopTime=None):
		self.Logger = logger
		self.PickSimulation(simNumber)
		self.StopTime = stopTime
		self.outcomePredictor = None

		#setting
		self.NumberOfBots = self.SimInfo["MaxPlayers"]
		self.LastOutputTime = time.time()
		self.LastSaveTook = 0
		self.WinningMode = False

		self.AiDataManager = DataSetManager.DataSetManager(self.Logger, self.SimInfo["NumInputs"], self.SimInfo["MinInputSize"],
                                                     self.SimInfo["MaxInputSize"], self.SimInfo["Resolution"], self.SimInfo["SimName"])

		if self.SimInfo["RenderSetup"]:
			if renderQuality != None:
				self.RenderQuality = renderQuality
			else:
				self.RenderQuality = int(input("no Output 0): Simple 1): Complex 2):"))
		else:
			self.RenderQuality = 0


		self.SetupAgent(loadData, aiType, trainNetwork)


		if self.RenderQuality == 2:
			import RenderEngine.RenderEngine2D as RenderEngine
			self.RenderEngine = RenderEngine.RenderEngine()

		elif self.RenderQuality == 0:
			self.Logger.Clear()

		return

	def SetupAgent(self, loadData=None, aiType=None, trainNetwork=None):
		if aiType == None:
			userInput = input("Brute B) Network N) Evolution E) Random R) See Tree T) Human H) MonteCarloAgent M):")
		else:
			userInput = aiType

		userInput = userInput.upper()

		self.Agents = []

		if userInput == "T":
			loadData = self.SetUpMetaData("Y")
			if loadData:
				import RenderEngine.TreeVisualiser as TreeVisualiser
				TreeVisualiser.TreeVisualiser(self.AiDataManager)

			input("hold here error!!!!!")


		else:
			loadData = self.SetUpMetaData(loadData)
			import Agents.SimOutputPredictor as SimOutputPredictor
			self.OutcomePredictor = SimOutputPredictor.SimOutputPredictor(self.AiDataManager, loadData)

			if userInput == "H":
				self.WinningMode = True
				self.Agents += [HumanAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]

				for loop in range(self.NumberOfBots-1):
					self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]


			elif userInput == "R":
				self.Agents += [RandomAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]

				for loop in range(self.NumberOfBots-1):
					self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]

			elif userInput == "N":
				if trainNetwork == None:
					userInput = input("Train Network[Y/N]: ")
				else:
					userInput = trainNetwork

				import Agents.NeuralNetworkAgent as NeuralNetwork
				trainingMode = userInput == "Y" or userInput == "y"
				
				self.Agents += [NeuralNetwork.Agent(self.AiDataManager, loadData, 
					winningModeON=self.WinningMode, trainingMode=trainingMode)]

				for loop in range(self.NumberOfBots-1):
					self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]

			elif userInput.upper() == "E":
				import Agents.Evolution.EvolutionAgent as EvolutionAgent
				import Agents.Evolution.EvolutionController as EvolutionController
				evoController = EvolutionController.EvolutionController(self.AiDataManager, loadData, winningModeON=self.WinningMode)

				self.Agents += [EvolutionAgent.Agent(evoController, self.AiDataManager, loadData, winningModeON=self.WinningMode)]

				for loop in range(self.NumberOfBots-1):
					self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]

			elif userInput.upper() == "M":
				import Agents.MonteCarloAgent as MonteCarloAgent
				moveAgent = BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)

				self.Agents += [MonteCarloAgent.Agent(self.AiDataManager, loadData, moveAgent, winningModeON=self.WinningMode)]

				for loop in range(self.NumberOfBots-1):
					self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]


			else:
				for loop in range(self.NumberOfBots):
					self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData, winningModeON=self.WinningMode)]

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

		self.Logger.SetTitle("AI Playing:"+self.SimInfo["SimName"])

		return
	def SetUpMetaData(self, loadData=None):
		userInput = "N"

		if self.AiDataManager.LoadMetaData():
			if self.AiDataManager.MetaDataGet("Version") == self.Version:
				if loadData == None:
					self.Logger.Clear()
					print("")
					print("SizeOfDataSet: "+str(self.AiDataManager.MetaDataGet("SizeOfDataSet")))
					print("NumberOfCompleteBoards: "+str(self.AiDataManager.MetaDataGet("NumberOfCompleteBoards")))
					print("NumberOfFinishedBoards: "+str(self.AiDataManager.MetaDataGet("NumberOfFinishedBoards")))
					print("NumberOfGames: "+str(self.AiDataManager.MetaDataGet("NumberOfGames")))
					print("TotalTime: "+Format.SplitTime(self.AiDataManager.MetaDataGet("TotalTime"), roundTo=2))
					print("LastBackUpTotalTime: "+Format.SplitTime(self.AiDataManager.MetaDataGet("LastBackUpTotalTime"), roundTo=2))
					print("")
					userInput = input("load Dataset[Y/N]:")
				else:
					userInput = loadData
			else:
				print("MetaData Version "+str(self.AiDataManager.MetaDataGet("Version"))+" != AiVersion "+str(self.Version)+" !")
				input()

		if userInput == "n" or userInput == "N":
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
			self.AiDataManager.MetaDataSet("AnnDataMadeFromTotalTime", 0)
			self.AiDataManager.MetaDataSet("LastBackUpTotalTime", 0)
			self.AiDataManager.MetaDataSet("AnnMoveInputShape", None)
			self.AiDataManager.MetaDataSet("AnnMoveStructreArray", None)
			self.AiDataManager.MetaDataSet("AnnRunId", None)
			self.AiDataManager.MetaDataSet("TriedMovesPlayed", 0)
			self.AiDataManager.MetaDataSet("VaildMovesPlayed", 0)
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

	def Output(self, agents, outcomePredictor, game, numMoves, gameStartTime, board, turn, finished=False):
		if self.RenderQuality == 0:
			return
		if (time.time() - self.LastOutputTime) >= 0.5 or self.WinningMode:
			numGames = self.AiDataManager.MetaDataGet("NumberOfGames")+1

			backUpTime = self.AiDataManager.MetaDataGet("LastBackUpTotalTime")
			totalTime = self.AiDataManager.MetaDataGet("TotalTime")
			realTime = self.AiDataManager.MetaDataGet("RealTime")
			numberOfCompleteBoards = self.AiDataManager.MetaDataGet("NumberOfCompleteBoards")
			numberOfFinishedBoards = self.AiDataManager.MetaDataGet("NumberOfFinishedBoards")
			avgMoveTime = 0
			if numMoves != 0:
				avgMoveTime = (time.time() - gameStartTime)/numMoves
				avgMoveTime = round(avgMoveTime, 6)

			self.Logger.Clear()
			self.RenderBoard(game, board)
			print("")
			print("Dataset size: " + str(Format.SplitNumber(self.AiDataManager.GetNumberOfBoards())))
			print("Number Of Complete Boards: " + str(Format.SplitNumber(numberOfCompleteBoards)))
			print("Number Of Finished Boards: " + str(Format.SplitNumber(numberOfFinishedBoards)))
			if finished:
				print("game: " + str(Format.SplitNumber(numGames)) + " move: " + str(Format.SplitNumber(numMoves)) + " finished game")
			else:
				print("game: " + str(Format.SplitNumber(numGames)) + " move: " + str(Format.SplitNumber(numMoves)))
			print("moves avg took: " + str(avgMoveTime) + " seconds")
			print("Games avg took: " + Format.SplitTime(totalTime/numGames, roundTo=6))
			print("time since start: " + Format.SplitTime(totalTime))
			print("Real Time since start: " + Format.SplitTime(realTime))

			print("time since last BackUp: " + Format.SplitTime(totalTime-backUpTime))

			for loop in range(len(agents)):
				print()
				print("Agent["+str(loop)+"] ("+str(agents[loop].AgentType)+") Info: ")
				print(agents[loop].AgentInfoOutput())

			print()
			print("Predictor")
			print(outcomePredictor.PredictorInfoOutput())
			
			title = "AI Playing: "+self.SimInfo["SimName"]
			title += " Time Since Last Save: " + Format.SplitTime(time.time()-self.LastSaveTime, roundTo=1)
			title += " CachingInfo: " + self.AiDataManager.GetLoadedDataInfo()
			title += " LastSaveTook: " + Format.SplitTime(self.LastSaveTook)
			self.Logger.SetTitle(title)
			self.LastOutputTime = time.time()

		elif self.RenderQuality == 2:
			self.RenderBoard(game, board)


		return
	
	def RunTraning(self):
		targetThreadNum = 1
		gamesToPlay = 100
		self.LastSaveTime = time.time()

		startTime = time.time()

		while not (self.StopTime != None and time.time()-startTime >= self.StopTime):

			threads = []
			for loop in range(targetThreadNum-1):
				game = self.Sim.CreateNew()
				agents = []
				#todo make agent list again from user input from before
				for loop in range(self.NumberOfBots):
					agents += [BruteForceAgent.Agent(self.AiDataManager, False, winningModeON=self.WinningMode)]
				thread = threading.Thread(target=self.RunSimTournament, args=(gamesToPlay, game, agents, self.OutcomePredictor, False,))
				threads += [thread]
				thread.start()


			self.RunSimTournament(gamesToPlay, self.Sim, self.Agents, self.OutcomePredictor, True)
			for thread in threads:
				thread.join()

		self.TrySaveData(True)
		return

	def RunSimTournament(self, gamesToPlay, game, agents, outcomePredictor, isMainThread):
		board, turn = game.Start()
		self.AiDataManager.UpdateStartingBoards(board)

		numMoves = 0
		numGames = 0
		totalStartTime = time.time()
		gameStartTime = time.time()
		while gamesToPlay == -1 or numGames < gamesToPlay:
			if isMainThread:
				self.Output(agents, outcomePredictor, game, numMoves, gameStartTime, board, turn)
			board, turn, finished, fit = MakeAgentMove(turn, board, agents, outcomePredictor, game)

			numMoves += 1
			temp = time.time()-totalStartTime
			self.AiDataManager.MetaDataAdd("TotalTime", temp)
			if isMainThread:
				self.AiDataManager.MetaDataAdd("RealTime", temp)
			totalStartTime = time.time()

			if finished:
				numGames += 1
				self.AiDataManager.MetaDataAdd("NumberOfGames", 1)

				for loop in range(len(agents)):
					agents[loop].GameFinished(fit[loop])

				if isMainThread:
					self.Output(agents, outcomePredictor, game, numMoves, gameStartTime, board, turn, finished=True)

					self.TrySaveData()

				if self.StopTime != None and self.AiDataManager.MetaDataGet("RealTime") >= self.StopTime:
					break

				board, turn = game.Start()
				self.AiDataManager.UpdateStartingBoards(board)
				numMoves = 0
				gameStartTime = time.time()
		
		for loop in range(len(agents)):
			agents[loop].TournamentFinished()
		return

	def TrySaveData(self, forceSave=False):
		if time.time()-self.LastSaveTime > 60 or forceSave:
			self.LastSaveTook = time.time()


			# save back up every hour
			if self.AiDataManager.MetaDataGet("TotalTime")-self.AiDataManager.MetaDataGet("LastBackUpTotalTime") > 60*60:
				self.AiDataManager.BackUp()

			self.AiDataManager.Save()
			self.LastSaveTime = time.time()
			self.LastSaveTook = time.time() - self.LastSaveTook
		return


if __name__ == "__main__":
	Logger = Logger.Logger()
	Logger.Clear()
	hadError = False

	try:
		controller = RunController(Logger, renderQuality=1, simNumber=None, loadData="Y", aiType=None, stopTime=None)

	except Exception as error:
		Logger.LogError(error)
		hadError= True

	if not hadError:
		try:
			controller.RunTraning()

		except Exception as error:
			Logger.LogError(error)
