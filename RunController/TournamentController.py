import time
from DataManger.Serializer import BoardToKey
from Shared import OutputFormating as Format
import RunController.eRenderType as eRenderType

class TournamentController:

	AgentOrderPermutations = []

	def __init__(self, logger, metricsLogger, game, agents, dataManager, outcomePredictor, renderQuality):
		self.Logger = logger
		self.MetricsLogger = metricsLogger

		self.Game = game
		self.Agents = agents
		self.DataManager = dataManager

		self.OutcomePredictor = outcomePredictor
		self.RenderQuality = renderQuality

		self.AgentOrderPermutations = GetAllPermutations(self.Agents)
		#todo? should these be moved
		self.LastSaveTime = time.time()
		self.LastOutputTime = time.time()
		self.MoveNumber = 0
		self.LastSaveTook = 0

		self.OutputFrameCount = 0
		self.TotalOutputTime = 0

		if self.RenderQuality == eRenderType.eRenderType.RenderOutput:
			import RenderEngine.RenderEngine2D as RenderEngine
			self.RenderEngine = RenderEngine.RenderEngine()

		self.MetricsLogger.Log("RenderQuality", self.RenderQuality.value)
		return

	def RunTournament(self, targetGameCount, stopTime=None):
		
		gameCount = 0
		while ((targetGameCount == -1 or gameCount < targetGameCount) and
			(stopTime == None or self.DataManager.MetaDataGet("RealTime") >= stopTime)):

			timeMark  = time.time()

			permutationIndex = gameCount % len(self.AgentOrderPermutations)
			agents = self.AgentOrderPermutations[permutationIndex]

			self.RunGame(agents)
			self.MetricsLogger.Log("GameTook", time.time()-timeMark)

			gameCount += 1

		for agent in self.Agents:
			agent.TournamentFinished()
		return

	def RunGame(self, agents):
		board, turn = self.Game.Start()
		self.DataManager.UpdateStartingBoards(board)

		totalTime = time.time()

		self.GameFinished = False
		self.MoveNumber = 0
		self.GameStartTime = time.time()
		while not self.GameFinished:
			self.Output(board)
			board, turn, self.GameFinished, fit = self.MakeAgentMove(
				turn, board, agents)
			self.MoveNumber += 1

			temp = time.time()-totalTime
			self.DataManager.MetaDataAdd("TotalTime", temp)
			self.DataManager.MetaDataAdd("RealTime", temp)
			totalTime = time.time()


		#game has now finished

		self.DataManager.MetaDataAdd("NumberOfGames", 1)

		for loop in range(len(agents)):
			agents[loop].GameFinished(fit[loop])


		self.TrySaveData()

		self.MetricsLogger.Log("numTablesLoaded", len(self.DataManager.LoadedDataSetTables))
		self.MetricsLogger.Log("MovesCountPerGame", self.MoveNumber)
		self.MetricsLogger.DictLog(self.DataManager.MetaData.Content)
		return

	def MakeAgentMove(self, turn, board, agents):
		timeMark  = time.time()

		startBoardKey = BoardToKey(board)

		agent = agents[turn-1]
		valid = False
		while not valid:
			move = agent.MoveCal(board)
			
			self.OutcomePredictor.PredictOutput(board, move)

			valid, outComeBoard, turn = self.Game.MakeMove(move)

			if not valid:
				agent.UpdateInvalidMove(board, move)

				if self.OutcomePredictor != None:
					self.OutcomePredictor.UpdateInvalidMove(board, move)


		finished, fit = self.Game.CheckFinished()

		if self.OutcomePredictor != None:
			self.OutcomePredictor.UpdateMoveOutCome(startBoardKey, move, outComeBoard, finished)

		agent.UpdateMoveOutCome(startBoardKey, move, outComeBoard, finished)

		self.MetricsLogger.Log("Agent"+str(agent.AgentNumber)+"MoveTook", time.time()-timeMark)
		return outComeBoard, turn, finished, fit

	def RenderBoard(self, board):
		if self.RenderQuality == eRenderType.eRenderType.Muted:
			return

		elif (self.RenderQuality == eRenderType.eRenderType.ArrayOutput):
			print(board)

		elif (self.RenderQuality == eRenderType.eRenderType.TextOutput or 
			self.RenderQuality ==eRenderType.eRenderType.CustomOutput):
			
			self.Game.SimpleBoardOutput(board)
		
		elif self.RenderQuality == eRenderType.eRenderType.RenderOutput:

			timeMark = time.time()
			self.RenderEngine.PieceList = self.Game.ComplexBoardOutput(board)
			timeMark = time.time()-timeMark
			if not self.RenderEngine.UpdateWindow(timeMark):
				self.RenderQuality = 0
		return

	def Output(self, board):
		outputTime = time.time()

		if self.RenderQuality == eRenderType.eRenderType.Muted:
			return

		if (time.time() - self.LastOutputTime) < 0.5:
			if (self.RenderQuality == eRenderType.eRenderType.RenderOutput or
				self.RenderQuality == eRenderType.eRenderType.CustomOutput):

				self.RenderBoard(board)

		else:
			self.Logger.Clear()

			self.RenderBoard(board)

			numGames = self.DataManager.MetaDataGet("NumberOfGames")+1
			backUpTime = self.DataManager.MetaDataGet("LastBackUpTotalTime")
			totalTime = self.DataManager.MetaDataGet("TotalTime")
			realTime = self.DataManager.MetaDataGet("RealTime")
			numberOfCompleteBoards = self.DataManager.MetaDataGet("NumberOfCompleteBoards")
			numberOfFinishedBoards = self.DataManager.MetaDataGet("NumberOfFinishedBoards")
			avgMoveTime = 0
			if self.MoveNumber != 0:
				avgMoveTime = (time.time() - self.GameStartTime)/self.MoveNumber
				avgMoveTime = round(avgMoveTime, 6)

			print("")
			print("Dataset size: " + str(Format.SplitNumber(self.DataManager.GetNumberOfBoards())))
			print("Number Of Complete Boards: " + str(Format.SplitNumber(numberOfCompleteBoards)))
			print("Number Of Finished Boards: " + str(Format.SplitNumber(numberOfFinishedBoards)))
			print("games: " + str(Format.SplitNumber(numGames)) + " moves: " + str(Format.SplitNumber(self.MoveNumber)))
			print("moves avg took: " + str(avgMoveTime) + " seconds")
			print("Games avg took: " + Format.SplitTime(totalTime/numGames, roundTo=6))
			print("time since start: " + Format.SplitTime(totalTime))
			print("Real Time since start: " + Format.SplitTime(realTime))
			print("time since last BackUp: " + Format.SplitTime(totalTime-backUpTime))

			for loop in range(len(self.Agents)):
				print()
				print("Agent["+str(loop)+"] ("+str(self.Agents[loop].AgentType)+") Info: ")
				print(self.Agents[loop].AgentInfoOutput())

			print()
			print("OutcomePredictor")
			print(self.OutcomePredictor.PredictorInfoOutput())
			
			title = self.Game.Info["SimName"]
			title += " Time Since Last Save: " + Format.SplitTime(time.time()-self.LastSaveTime, roundTo=1)
			title += " CachingInfo: " + self.DataManager.GetLoadedDataInfo()
			title += " LastSaveTook: " + Format.SplitTime(self.LastSaveTook)
			self.Logger.SetTitle(title)

			self.LastOutputTime = time.time()

			avgOutputTime = 0
			
			if self.OutputFrameCount != 0:
				avgOutputTime = self.TotalOutputTime / self.OutputFrameCount

			print()
			print("Output avg Took: "+ Format.SplitTime(avgOutputTime, roundTo=4))
			self.MetricsLogger.Log("AvgOutputTime", avgOutputTime)

	
		self.OutputFrameCount += 1
		self.TotalOutputTime += time.time()-outputTime

		if self.OutputFrameCount >= 100000:
			self.TotalOutputTime = self.TotalOutputTime / self.OutputFrameCount
			self.OutputFrameCount = 1000
			self.TotalOutputTime *= self.OutputFrameCount
		return

	def TrySaveData(self, forceSave=False):
		if time.time()-self.LastSaveTime > 60 or forceSave:
			self.LastSaveTook = time.time()


			# save back up every hour
			if self.DataManager.MetaDataGet("TotalTime")-self.DataManager.MetaDataGet("LastBackUpTotalTime") > 60*60:
				timeMark = time.time()
				self.DataManager.BackUp()
				self.MetricsLogger.Log("BackUpSavingTime", time.time()-timeMark)

			timeMark = time.time()
			self.DataManager.Save()
			self.MetricsLogger.Log("SavingTime", time.time()-timeMark)

			learnedDataSize = self.DataManager.GetSizeOfLearnedDataSize()
			self.MetricsLogger.Log("LearnedDataDiskSize", learnedDataSize)

			self.LastSaveTime = time.time()
			# todo make this give avg save time
			self.LastSaveTook = time.time() - self.LastSaveTook
		return

def GetAllPermutations(elements):

	if len(elements) <= 1:
		return elements

	output = []
	index = 0
	while index < len(elements):
		temp = elements[:]
		del temp[index]

		for permutation in [GetAllPermutations(temp)]:
			output += [[elements[index]]+permutation]

		index += 1

	return output
