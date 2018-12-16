import BruteForce as AI
import Draughts as Game
import time
import os


class RunController(object):
	def __init__(self):
		#setting 
		self.RenderQuality = 0
		self.NumberOfBots = 2

		self.WinningMode = False
		if self.NumberOfBots == 1:
			self.WinningMode = True

		self.AiDataManager = AI.DataSetManager(4, 8)

		if self.RenderQuality == 2:
			import RenderEngine
			self.RenderEngine = RenderEngine.RenderEngine()


		self.GameLoop()
		return

	def Render(self, board=None, turn=None):
		if self.RenderQuality == 1 and board != None:
			os.system("cls")
			Game.SimpleOutput(board)

		elif self.RenderQuality == 2:
			if board !=None and turn != None:
				self.RenderEngine.UpdateBoard(board, turn)
			self.RenderEngine.UpdateFrame()
			self.RenderEngine.UpdateConsoleText("test\ntest")

		return

	def MakeAIMove(self, turn, board, AIs, game):
		AI = AIs[turn-1]

		valid = False
		if turn == 1:
			while not valid:
				move = AI.MoveCal(game.FlipBoard())
				valid, board, step = game.MakeSelection(move[0], move[1])
				if not valid:
					AI.UpdateInvalidMove(game.FlipBoard(), move)
				else:
					valid, board, turn, step = game.MakeMove(move[2], move[3])
					if not valid:
						AI.UpdateInvalidMove(game.FlipBoard(), move)
		else:
			while not valid:
				move = AI.MoveCal(board)
				valid, board, step = game.MakeSelection(move[0], move[1])
				if not valid:
					AI.UpdateInvalidMove(board, move)
				else:
					valid, board, turn, step = game.MakeMove(move[2], move[3])
					if not valid:
						AI.UpdateInvalidMove(board, move)
		return board, turn
	
	def MakeHumanMove(self, game):
		if self.RenderQuality == 2:
			board, turn = self.RenderEngine.MakeHumanMove(game)
		return board, turn

	def GameLoop(self):
		game = Game.Draughts()
		AIs = []
		AIs += [AI.BruteForce(self.AiDataManager, winningModeON=self.WinningMode)]
		AIs += [AI.BruteForce(self.AiDataManager, winningModeON=self.WinningMode)]
		board, turn, _ = game.start()

		self.Render(board=board, turn=turn)

		
		numGames = 0
		numMoves = 0

		time_taken = time.time()
		MoveTime = time.time()
		while True:
			if self.NumberOfBots >= turn:
				board, turn = self.MakeAIMove(turn, board, AIs, game)
			else:
				board, turn = self.MakeHumanMove(game)

			self.Render(board=board, turn=turn)

			numMoves += 1
			if numMoves % 50 == 0:
				print("done " + str(numMoves) + " moves took on AVG: " + str((time.time() - MoveTime)/50) + " seconds")
				MoveTime = time.time()

			finished, fit = game.CheckFinished()

			if finished:

				print("")
				for loop in range(len(AIs)):
					AIs[loop].UpdateData(fit[loop])

				print("finished game: " + str(numGames+1) + " with " + str(numMoves) + " moves made")
				print("each move took on AVG: " + str((time.time() - time_taken)/numMoves) + " seconds")
				print("game in total took: " + str(time.time() - time_taken) + " seconds")

				board, turn, _ = game.start()
				numGames += 1
				numMoves = 0

				print("")
				print("")
				time_taken = time.time()
				MoveTime = time.time()
		return

if __name__ == "__main__":
	RunController()