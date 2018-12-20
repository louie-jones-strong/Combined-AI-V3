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

		
		self.AiDataManager = AI.DataSetManager(4, 8,loadData=False)

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

		return

	def MakeAIMove(self, turn, board, AIs, game):
		testing = time.time()
		temploop = 0
		testtemp = turn

		AI = AIs[turn-1]

		valid = False
		if turn == 1:
			mark1 = time.time()
			while not valid:
				temploop += 1
				game.FlipBoard()
				print("flipboard:          " + str(time.time()-mark1))
				
				move = game.FlipInput(AI.MoveCal(game.FlipBoard()))
				print("ai.movecal:         " + str(time.time()-mark1))

				mark2 = time.time()
				valid, board, step = game.MakeSelection(move[0], move[1])
				print("game.MakeSelection: " + str(time.time()-mark2))

				if not valid:
					mark3 = time.time()
					AI.UpdateInvalidMove(game.FlipBoard(), move)
					print("UpdateInvalidMove:  " + str(time.time()-mark3))
				else:
					mark4 = time.time()
					valid, board, turn, step = game.MakeMove(move[2], move[3])
					print("game.MakeSelection: " + str(time.time()-mark4))
					if not valid:
						mark3 = time.time()
						AI.UpdateInvalidMove(game.FlipBoard(), move)
						print("UpdateInvalidMove: " + str(time.time()-mark3))

				input("move took:          " + str(time.time()-mark1) + ": ")
				print("")
				mark1 = time.time()
			
			input("testing input: " + str(time.time()-testing) + " tried: " + str(temploop) + " times turn:" + str(testtemp) + ": ")
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
			if numMoves % 10 == 0:
				print("done " + str(numMoves) + " moves took on AVG: " + str((time.time() - MoveTime)/10) + " seconds")

				MoveTime = time.time()
				
			if self.RenderQuality == 2:
				self.RenderEngine.UpdateConsoleText("Game: "+str(numGames)+"\n Move: "+str(numMoves)+"\n AVG time: "+str((time.time() - time_taken)/numMoves))

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