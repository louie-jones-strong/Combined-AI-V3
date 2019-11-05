import time
from DataManger.Serializer import BoardToKey
from Shared import OutputFormating as Format


class TournamentController:

	def __init__(self, logger, game, agents, dataManager, outcomePredictor, renderQuality):
		self.Logger = logger
		self.Game = game
		self.Agents = agents
		self.DataManager = dataManager

		self.OutcomePredictor = outcomePredictor
		self.RenderQuality = renderQuality

		#todo? should these be moved
		self.LastSaveTime = time.time()
		self.LastOutputTime = time.time()
		self.MoveNumber = 0

		if self.RenderQuality == 3:
			import RenderEngine.RenderEngine2D as RenderEngine
			self.RenderEngine = RenderEngine.RenderEngine()
		return

	def RunTournament(self, numGames):
		
		for loop in range(numGames):
			self.RunGame()

		for agent in self.Agents:
			agent.TournamentFinished()
		return

	def RunGame(self):
		board, turn = self.Game.Start()
		self.DataManager.UpdateStartingBoards(board)

		totalTime = time.time()

		self.GameFinished = False
		self.MoveNumber = 0
		self.GameStartTime = time.time()
		while not self.GameFinished:
			self.Output(board)
			board, turn, self.GameFinished, fit = self.MakeAgentMove(turn, board)
			self.MoveNumber += 1

			temp = time.time()-totalTime
			self.DataManager.MetaDataAdd("TotalTime", temp)
			totalTime = time.time()


		#game has now finished

		self.DataManager.MetaDataAdd("NumberOfGames", 1)

		for loop in range(len(self.Agents)):
			self.Agents[loop].GameFinished(fit[loop])

		self.TrySaveData()
		return

	def MakeAgentMove(self, turn, board):
		startBoardKey = BoardToKey(board)

		agent = self.Agents[turn-1]
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

		return outComeBoard, turn, finished, fit

	def RenderBoard(self, board):
		if self.RenderQuality == 0:
			return

		elif self.RenderQuality == 2:
			self.Game.SimpleBoardOutput(board)
		
		elif self.RenderQuality == 3:
			timeMark = time.time()
			self.RenderEngine.PieceList = self.Game.ComplexBoardOutput(board)
			timeMark = time.time()-timeMark
			if not self.RenderEngine.UpdateWindow(timeMark):
				self.RenderQuality = 0
		return

	def Output(self, board):
		outputTime = time.time()

		if self.RenderQuality == 0:
			return

		if (time.time() - self.LastOutputTime) < 0.5:
			if self.RenderQuality == 3:
				self.RenderBoard(board)
			return

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
		
		title = self.Game.SimInfo["SimName"]
		title += " Time Since Last Save: " + Format.SplitTime(time.time()-self.LastSaveTime, roundTo=1)
		title += " CachingInfo: " + self.DataManager.GetLoadedDataInfo()
		title += " LastSaveTook: " + Format.SplitTime(self.LastSaveTook)
		self.Logger.SetTitle(title)

		outputTime = time.time()-outputTime
		print()
		print("Output Took: "+ Format.SplitTime(outputTime))
		self.LastOutputTime = time.time()
		return

	def TrySaveData(self, forceSave=False):
		if time.time()-self.LastSaveTime > 60 or forceSave:
			self.LastSaveTook = time.time()


			# save back up every hour
			if self.DataManager.MetaDataGet("TotalTime")-self.DataManager.MetaDataGet("LastBackUpTotalTime") > 60*60:
				self.DataManager.BackUp()

			self.DataManager.Save()
			self.LastSaveTime = time.time()
			# todo make this give avg save time
			self.LastSaveTook = time.time() - self.LastSaveTook
		return