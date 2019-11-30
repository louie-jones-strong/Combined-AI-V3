import DataManger.DataSetManager as DataSetManager
from Shared import OutputFormating as Format
import importlib
import time
import os
import RunController.eRenderType as eRenderType
import RunController.eLoadType as eLoadType
import RunController.eAgentType as eAgentType
import RunController.TournamentController as TournamentController

class RunController:

	Version = 1.6

	def __init__(self, logger, metricsLogger, agentSetupData, simNumber=None, loadType=eLoadType.eLoadType.Null, renderQuality=eRenderType.eRenderType.Null, trainNetwork=None, stopTime=None):
		self.Logger = logger
		self.MetricsLogger = metricsLogger
		self.PickSimulation(simNumber)
		self.StopTime = stopTime
		self.outcomePredictor = None

		#setting
		self.NumberOfAgents = self.SimInfo["MaxPlayers"]

		self.DataManager = DataSetManager.DataSetManager(self.Logger, self.SimInfo)

		if renderQuality != eRenderType.eRenderType.Null:
			if not self.SimInfo["RenderSetup"] and renderQuality.value >= eRenderType.eRenderType.CustomOutput.value:
				self.RenderQuality = eRenderType.eRenderType.TextOutput
			else:
				self.RenderQuality = renderQuality
		else:
			if self.SimInfo["RenderSetup"]:
				temp = int(input("Muted 1) just info 2) Raw 3) Text 4) custom 5) pygame 6): "))

			else:
				temp = int(input("Muted 1) just info 2) Raw 3) Text 4): "))

			self.RenderQuality = eRenderType.FromInt(temp)

		loadData = self.SetUpMetaData(loadType)
		
		import Predictors.SimOutputPredictor as SimOutputPredictor
		self.OutcomePredictor = SimOutputPredictor.SimOutputPredictor(self.DataManager, loadData)

		self.EvoController = None

		self.Agents = []
		for loop in range(self.NumberOfAgents):
			if loop >= len(agentSetupData):
				agentData = agentSetupData[len(agentSetupData)-1]
			else:
				agentData = agentSetupData[loop]

			print("")
			print("Setting up Agent["+str(loop)+"]...")
			self.Agents += [self.SetupAgent(agentData, loadData)]

		if loadData:
			runId = self.DataManager.MetaDataGet("RunId")
		else:
			runId = self.SimInfo["SimName"] +"_"+ Format.TimeToDateTime(time.time(),True, True, 
				dateSplitter="_", timeSplitter="_", dateTimeSplitter="_")

		self.MetricsLogger.RunSetup(runId, loadData)

		loop = 0
		for agent in self.Agents:
			self.MetricsLogger.Log("Agent"+str(loop)+" Type", agent.AgentType)
			loop += 1


		self.DataManager.MetaDataSet("RunId", runId)
		self.Logger.Clear()

		return

	def SetupAgent(self, agentData, loadData):
		agent = None

		agentType = agentData.GetType()

		if agentType == eAgentType.eAgentType.Human:
			import Agents.HumanAgent as HumanAgent

			agent = HumanAgent.Agent(self.DataManager, loadData, winningModeON=True)

		elif agentType == eAgentType.eAgentType.BruteForce:
			import Agents.BruteForceAgent as BruteForceAgent

			agent = BruteForceAgent.Agent(self.DataManager, loadData)

		elif agentType == eAgentType.eAgentType.Random:
			import Agents.RandomAgent as RandomAgent

			agent = RandomAgent.Agent(self.DataManager, loadData)

		elif agentType == eAgentType.eAgentType.NeuralNetwork:
			import Agents.NeuralNetworkAgent as NeuralNetwork
			
			agent = NeuralNetwork.Agent(self.DataManager, loadData, trainingMode=agentData.GetPlayingMode())

		elif agentType == eAgentType.eAgentType.Evolution:
			import Agents.Evolution.EvolutionAgent as EvolutionAgent

			if self.EvoController == None:
				import Agents.Evolution.EvolutionController as EvolutionController
				
				self.EvoController = EvolutionController.EvolutionController(self.DataManager, loadData)

			agent = EvolutionAgent.Agent(self.EvoController, self.DataManager, loadData)
			
		elif agentType == eAgentType.eAgentType.MonteCarlo:
			import Agents.MonteCarloAgent as MonteCarloAgent

			print("Setting up SubAgent")
			moveAgent = self.SetupAgent(agentData.GetSubMoveAgent(),loadData)

			agent = MonteCarloAgent.Agent(self.DataManager, loadData, moveAgent)

		return agent

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
	def SetUpMetaData(self, loadType):
		if self.DataManager.LoadMetaData():

			if self.DataManager.MetaDataGet("Version") == self.Version:
				if loadType == eLoadType.eLoadType.Null:
					self.Logger.Clear()
					print("")
					print("SizeOfDataSet: "+str(self.DataManager.MetaDataGet("SizeOfDataSet")))
					print("NumberOfCompleteBoards: "+str(self.DataManager.MetaDataGet("NumberOfCompleteBoards")))
					print("NumberOfFinishedBoards: "+str(self.DataManager.MetaDataGet("NumberOfFinishedBoards")))
					print("NumberOfGames: "+str(self.DataManager.MetaDataGet("NumberOfGames")))
					print("TotalTime: "+Format.SplitTime(self.DataManager.MetaDataGet("TotalTime"), roundTo=2))
					print("LastBackUpTotalTime: "+Format.SplitTime(self.DataManager.MetaDataGet("LastBackUpTotalTime"), roundTo=2))
					print("")

					if input("load Dataset[Y/N]:").capitalize() == "N":
						loadType = eLoadType.eLoadType.NotLoad
					else:
						loadType = eLoadType.eLoadType.Load

			else:
				print("MetaData Version "+str(self.DataManager.MetaDataGet("Version"))+" != AiVersion "+str(self.Version)+" !")
				input()
				loadType = eLoadType.eLoadType.NotLoad
		
		else:
			loadType = eLoadType.eLoadType.NotLoad

		if loadType == eLoadType.eLoadType.NotLoad:
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
			self.DataManager.MetaDataSet("RunId", "runId")
			return False
		
		return True

	def RunTraning(self):
		gamesToPlay = 100
		self.LastSaveTime = time.time()

		startTime = time.time()
		
		tournamentController = TournamentController.TournamentController(self.Logger, self.MetricsLogger, 
			self.Sim, self.Agents, self.DataManager, self.OutcomePredictor, self.RenderQuality)

		while not (self.StopTime != None and time.time()-startTime >= self.StopTime):

			tournamentController.RunTournament(gamesToPlay, self.StopTime)

		tournamentController.TrySaveData(True)
		return
