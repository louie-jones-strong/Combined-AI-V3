import time


class TournamentController:

	def __init__(self):
		self.Logger = logger
		self.Game = game
		self.Agents = Agents
		self.DataManager = dataManager


		#todo? should these be moved
		self.LastSaveTime = time.time()
		return

	def RunTournament(self):
		
		

		for agent in self.Agents:
			agent.TournamentFinished()
		return

	def RunGame(self):
		board, turn = self.Game.Start()
		self.DataManager.UpdateStartingBoards(board)

		totalTime = time.time()

		self.GameFinished = False
		while not self.GameFinished:
			self.Output()
			board, turn, self.GameFinished, fit = self.MakeAgentMove(turn, board)

			temp = time.time()-totalTime
			self.DataManager.MetaDataAdd("TotalTime", temp)
			totalTime = time.time()


		#game has now finished

		self.DataManager.MetaDataAdd("NumberOfGames", 1)

		for loop in range(len(self.Agents)):
			self.Agents[loop].GameFinished(fit[loop])

		self.TrySaveData()
		return

	def MakeAgentMove(self):

		return

	def Output(self):

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