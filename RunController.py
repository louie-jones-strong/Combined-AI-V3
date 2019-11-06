import Agents.BruteForceAgent as BruteForceAgent
import Agents.RandomAgent as RandomAgent
import Agents.HumanAgent as HumanAgent
import DataManger.DataSetManager as DataSetManager
from Shared import Logger
import importlib
import time
import os
from TournamentController import TournamentController

class RunController:

	Version = 1.5

	def __init__(self, logger, simNumber=None, loadData=None, aiType=None, renderQuality=None, trainNetwork=None, stopTime=None):
		self.Logger = logger
		self.PickSimulation(simNumber)
		self.StopTime = stopTime
		self.outcomePredictor = None

		#setting
		self.NumberOfAgents = self.SimInfo["MaxPlayers"]

		self.DataManager = DataSetManager.DataSetManager(self.Logger, self.SimInfo)

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
				TreeVisualiser.TreeVisualiser(self.DataManager)

			input("hold here error!!!!!")



		loadData = self.SetUpMetaData(loadData)
		import Predictors.SimOutputPredictor as SimOutputPredictor
		self.OutcomePredictor = SimOutputPredictor.SimOutputPredictor(self.DataManager, loadData)

		if userInput == "H":
			self.Agents += [HumanAgent.Agent(self.DataManager, loadData, winningModeON=True)]

			import Agents.MonteCarloAgent as MonteCarloAgent
			for loop in range(self.NumberOfAgents-1):
				moveAgent = BruteForceAgent.Agent(self.DataManager, loadData)

				self.Agents += [MonteCarloAgent.Agent(self.DataManager, loadData, moveAgent, winningModeON=True)]


		elif userInput == "R":
			self.Agents += [RandomAgent.Agent(self.DataManager, loadData)]

			for loop in range(self.NumberOfAgents-1):
				self.Agents += [BruteForceAgent.Agent(self.DataManager, loadData)]

		elif userInput == "N":
			if trainNetwork == None:
				userInput = input("Train Network[Y/N]: ")
			else:
				userInput = trainNetwork

			import Agents.NeuralNetworkAgent as NeuralNetwork
			trainingMode = userInput == "Y" or userInput == "y"
			
			self.Agents += [NeuralNetwork.Agent(self.DataManager, loadData, trainingMode=trainingMode)]

			for loop in range(self.NumberOfAgents-1):
				self.Agents += [BruteForceAgent.Agent(self.DataManager, loadData)]

		elif userInput == "E":
			import Agents.Evolution.EvolutionAgent as EvolutionAgent
			import Agents.Evolution.EvolutionController as EvolutionController
			evoController = EvolutionController.EvolutionController(self.DataManager, loadData)

			self.Agents += [EvolutionAgent.Agent(evoController, self.DataManager, loadData)]

			for loop in range(self.NumberOfAgents-1):
				self.Agents += [BruteForceAgent.Agent(self.DataManager, loadData)]

		elif userInput == "M":
			import Agents.MonteCarloAgent as MonteCarloAgent
			moveAgent = BruteForceAgent.Agent(self.DataManager, loadData)

			self.Agents += [MonteCarloAgent.Agent(self.DataManager, loadData, moveAgent)]

			for loop in range(self.NumberOfAgents-1):
				self.Agents += [BruteForceAgent.Agent(self.DataManager, loadData)]

		else:
			for loop in range(self.NumberOfAgents):
				self.Agents += [BruteForceAgent.Agent(self.DataManager, loadData)]

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

		if self.DataManager.LoadMetaData():
			if self.DataManager.MetaDataGet("Version") == self.Version:
				if loadData == None:
					self.Logger.Clear()
					print("")
					print("SizeOfDataSet: "+str(self.DataManager.MetaDataGet("SizeOfDataSet")))
					print("NumberOfCompleteBoards: "+str(self.DataManager.MetaDataGet("NumberOfCompleteBoards")))
					print("NumberOfFinishedBoards: "+str(self.DataManager.MetaDataGet("NumberOfFinishedBoards")))
					print("NumberOfGames: "+str(self.DataManager.MetaDataGet("NumberOfGames")))
					print("TotalTime: "+Format.SplitTime(self.DataManager.MetaDataGet("TotalTime"), roundTo=2))
					print("LastBackUpTotalTime: "+Format.SplitTime(self.DataManager.MetaDataGet("LastBackUpTotalTime"), roundTo=2))
					print("")
					userInput = input("load Dataset[Y/N]:")
				else:
					userInput = loadData
			else:
				print("MetaData Version "+str(self.DataManager.MetaDataGet("Version"))+" != AiVersion "+str(self.Version)+" !")
				input()

		if userInput == "n" or userInput == "N":
			self.DataManager.MetaDataSet("Version", self.Version)
			self.DataManager.MetaDataSet("SizeOfDataSet", 0)
			self.DataManager.MetaDataSet("NumberOfTables", 0)
			self.DataManager.MetaDataSet("FillingTable", 0)
			self.DataManager.MetaDataSet("NumberOfCompleteBoards", 0)
			self.DataManager.MetaDataSet("NumberOfFinishedBoards", 0)
			self.DataManager.MetaDataSet("NumberOfGames", 0)
			self.DataManager.MetaDataSet("NetworkUsingOneHotEncoding", False)
			self.DataManager.MetaDataSet("RealTime", 0)
			self.DataManager.MetaDataSet("TotalTime", 0)
			self.DataManager.MetaDataSet("BruteForceTotalTime", 0)
			self.DataManager.MetaDataSet("AnnTotalTime", 0)
			self.DataManager.MetaDataSet("AnnDataMadeFromTotalTime", 0)
			self.DataManager.MetaDataSet("LastBackUpTotalTime", 0)
			self.DataManager.MetaDataSet("AnnMoveInputShape", None)
			self.DataManager.MetaDataSet("AnnMoveStructreArray", None)
			self.DataManager.MetaDataSet("AnnRunId", None)
			self.DataManager.MetaDataSet("TriedMovesPlayed", 0)
			self.DataManager.MetaDataSet("VaildMovesPlayed", 0)
			return False
		
		return True

	def RunTraning(self):
		gamesToPlay = 100
		self.LastSaveTime = time.time()

		startTime = time.time()
		
		tournamentController = TournamentController(self.Logger, self.Sim, self.Agents, self.DataManager, self.OutcomePredictor, self.RenderQuality)

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
