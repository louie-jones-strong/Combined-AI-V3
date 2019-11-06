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
from TournamentController import TournamentController


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
		self.NumberOfAgents = self.SimInfo["MaxPlayers"]

		self.AiDataManager = DataSetManager.DataSetManager(self.Logger, self.SimInfo)

		if renderQuality != None:
			self.RenderQuality = renderQuality
		else:
			if self.SimInfo["RenderSetup"]:
				self.RenderQuality = int(input("no Output 0) Just Info 1) Simple 2) Complex 3): "))
			else:
				self.RenderQuality = int(input("no Output 0) Just Info 1): "))


		self.SetupAgent(loadData, aiType, trainNetwork)
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



		loadData = self.SetUpMetaData(loadData)
		import Predictors.SimOutputPredictor as SimOutputPredictor
		self.OutcomePredictor = SimOutputPredictor.SimOutputPredictor(self.AiDataManager, loadData)

		if userInput == "H":
			self.Agents += [HumanAgent.Agent(self.AiDataManager, loadData, winningModeON=True)]

			import Agents.MonteCarloAgent as MonteCarloAgent
			for loop in range(self.NumberOfAgents-1):
				moveAgent = BruteForceAgent.Agent(self.AiDataManager, loadData)

				self.Agents += [MonteCarloAgent.Agent(self.AiDataManager, loadData, moveAgent, winningModeON=True)]


		elif userInput == "R":
			self.Agents += [RandomAgent.Agent(self.AiDataManager, loadData)]

			for loop in range(self.NumberOfAgents-1):
				self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData)]

		elif userInput == "N":
			if trainNetwork == None:
				userInput = input("Train Network[Y/N]: ")
			else:
				userInput = trainNetwork

			import Agents.NeuralNetworkAgent as NeuralNetwork
			trainingMode = userInput == "Y" or userInput == "y"
			
			self.Agents += [NeuralNetwork.Agent(self.AiDataManager, loadData, trainingMode=trainingMode)]

			for loop in range(self.NumberOfAgents-1):
				self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData)]

		elif userInput == "E":
			import Agents.Evolution.EvolutionAgent as EvolutionAgent
			import Agents.Evolution.EvolutionController as EvolutionController
			evoController = EvolutionController.EvolutionController(self.AiDataManager, loadData)

			self.Agents += [EvolutionAgent.Agent(evoController, self.AiDataManager, loadData)]

			for loop in range(self.NumberOfAgents-1):
				self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData)]

		elif userInput == "M":
			import Agents.MonteCarloAgent as MonteCarloAgent
			moveAgent = BruteForceAgent.Agent(self.AiDataManager, loadData)

			self.Agents += [MonteCarloAgent.Agent(self.AiDataManager, loadData, moveAgent)]

			for loop in range(self.NumberOfAgents-1):
				self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData)]

		else:
			for loop in range(self.NumberOfAgents):
				self.Agents += [BruteForceAgent.Agent(self.AiDataManager, loadData)]

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

		self.Logger.SetTitle(self.SimInfo["SimName"])

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

	def RunTraning(self):
		gamesToPlay = 100
		self.LastSaveTime = time.time()

		startTime = time.time()
		
		tournamentController = TournamentController(self.Logger, self.Sim, self.Agents, self.AiDataManager, self.OutcomePredictor, self.RenderQuality)

		while not (self.StopTime != None and time.time()-startTime >= self.StopTime):

			tournamentController.RunTournament(gamesToPlay)

		tournamentController.TrySaveData(True)
		return

if __name__ == "__main__":
	Logger = Logger.Logger()
	Logger.Clear()
	hadError = False

	try:
		controller = RunController(Logger, renderQuality=3, simNumber=None, loadData="Y", aiType=None, stopTime=None)
		controller.RunTraning()

	except Exception as error:
		Logger.LogError(error)
