import BruteForce as AI
import importlib
import time
import os


class RunController(object):
	def __init__(self):
		files = os.listdir("Simulations")
		files.remove("__pycache__")
		files.remove("SimulationInterface.py")

		for loop in range(len(files)):
			files[loop] = files[loop][:-3]
			if len(files) > 1:
				print(str(loop+1)+") "+ files[loop])

		userInput = 1
		if len(files) > 1:
			userInput = int(input("pick Simulation: "))
			
		if userInput > len(files):
			userInput = len(files)

		if userInput < 1:
			userInput = 1

		simName = files[userInput-1]
		self.Sim = importlib.import_module("Simulations." + simName)
		datasetAddress = "DataSets//"+simName+"Dataset"

		userInput = input("load Dataset[Y/N]:")
		if userInput == "n" or userInput == "N":
			self.AiDataManager = AI.DataSetManager(4, 8, 1, datasetAddress, loadData=False)

		else:
			self.AiDataManager = AI.DataSetManager(4, 8, 1, datasetAddress, loadData=True)

		#setting 
		self.RenderQuality = 0
		self.NumberOfBots = 2

		self.WinningMode = False
		if self.NumberOfBots == 1:
			self.WinningMode = True


		if self.RenderQuality == 2:
			import RenderEngine
			self.RenderEngine = RenderEngine.RenderEngine()

		#self.testingTimes()
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

		AI = AIs[turn-1]

		valid = False
		if turn == 1:
			while not valid:
				move = AI.MoveCal(game.FlipBoard())
				flipedMove = game.FlipInput(move)
				valid, board = game.MakeSelection(flipedMove[0], flipedMove[1])

				if not valid:
					AI.UpdateInvalidMove(game.FlipBoard(), move)
				else:
					valid, board, turn = game.MakeMove(flipedMove[2], flipedMove[3])
					if not valid:
						AI.UpdateInvalidMove(game.FlipBoard(), move)
			
		else:
			while not valid:
				move = AI.MoveCal(board)
				valid, board = game.MakeSelection(move[0], move[1])

				if not valid:
					AI.UpdateInvalidMove(board, move)
				else:
					valid, board, turn = game.MakeMove(move[2], move[3])
					if not valid:
						AI.UpdateInvalidMove(board, move)
		return board, turn
	
	def MakeHumanMove(self, game):
		if self.RenderQuality == 2:
			board, turn = self.RenderEngine.MakeHumanMove(game)
		return board, turn

	def GameLoop(self):
		game = self.Sim.Simulation()
		AIs = []
		AIs += [AI.BruteForce(self.AiDataManager, winningModeON=self.WinningMode)]
		AIs += [AI.BruteForce(self.AiDataManager, winningModeON=self.WinningMode)]
		board, turn = game.Start()

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
			if numMoves % 50 == 0 or self.RenderQuality == 1:
				if self.RenderQuality == 1:
					print("done " + str(numMoves) + " moves, last took: " + str(time.time() - MoveTime) + " seconds")
				else: 
					print("done " + str(numMoves) + " moves took on AVG: " + str((time.time() - MoveTime)/50) + " seconds")

				MoveTime = time.time()
				
			if self.RenderQuality == 2:
				self.RenderEngine.UpdateConsoleText("Dataset Size: "+str(len(self.AiDataManager.DataSet))+"\n Game: "+str(numGames)+"\n Move: "+str(numMoves)+"\n AVG time: "+str((time.time() - time_taken)/numMoves))

			finished, fit = game.CheckFinished()
			if finished == False and numMoves >= 1000:
				finished = True
				fit = [3,3]

			if finished:

				print("")
				for loop in range(len(AIs)):
					AIs[loop].UpdateData(fit[loop])

				print("finished game: " + str(numGames+1) + " with " + str(numMoves) + " moves made")
				print("each move took on AVG: " + str((time.time() - time_taken)/numMoves) + " seconds")
				print("game in total took: " + str(time.time() - time_taken) + " seconds")

				board, turn = game.Start()
				numGames += 1
				numMoves = 0

				print("")
				print("")
				time_taken = time.time()
				MoveTime = time.time()
		return

	def testingTimes(self):
		game = self.Sim.Simulation()
		AIs = [AI.BruteForce(self.AiDataManager, winningModeON=self.WinningMode)]
		board, turn = game.Start()

		numberToRun = 4096
		print("running each for: " + str(numberToRun))

		mark1 = time.time()
		for loop in range(numberToRun):
			move = AIs[0].MoveCal(board)
		print("ai.movecal:        " + str((time.time()-mark1)))

		mark2 = time.time()
		for loop in range(numberToRun):
			game.FlipBoard()
		print("FlipBoard:         " + str((time.time()-mark2)))

		mark2 = time.time()
		for loop in range(numberToRun):
			game.FlipInput([0,0,0,0])
		print("Flipinput:         " + str((time.time()-mark2)))

		mark2 = time.time()
		for loop in range(numberToRun):
			AIs[0].UpdateInvalidMove(board, move)
		print("UpdateInvalidMove: " + str((time.time()-mark2)))

		mark2 = time.time()
		for loop in range(numberToRun):
			game.MakeSelection(move[0], move[1])
		print("MakeSelection:     " + str((time.time()-mark2)))

		mark2 = time.time()
		for loop in range(numberToRun):
			game.MakeMove(move[2], move[3])
		print("MakeMove:          " + str((time.time()-mark2)))
		input("total: " + str((time.time()-mark1)))

		mark2 = time.time()
		for loop in range(numberToRun):
			AIs[0].UpdateData(1)
		print("UpdateData:        " + str((time.time()-mark2)))

		print("total: " + str((time.time()-mark1)))
		input()
		return

if __name__ == "__main__":
	RunController()