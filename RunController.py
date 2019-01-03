import BruteForce as AI
import importlib
import time
import os
import sys

from threading import Thread

def MakeAIMove(turn, board, AIs, game):
	AI = AIs[turn-1]
	valid = False
	if turn == 1:
		while not valid:
			move = AI.MoveCal(game.FlipBoard())
			flipedMove = game.FlipInput(move)
			valid, board, turn = game.MakeMove(flipedMove)
			if not valid:
				AI.UpdateInvalidMove(game.FlipBoard(), move)
		
	else:
		while not valid:
			move = AI.MoveCal(board)
			valid, board, turn = game.MakeMove(move)
			if not valid:
				AI.UpdateInvalidMove(board, move)
	return board, turn

class RunController(object):
	def __init__(self):
		files = os.listdir("Simulations")
		if "__pycache__" in files:
			files.remove("__pycache__")

		if "SimulationInterface.py" in files:
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
		userInput = input("Render[Y/N]:")
		if userInput == "y" or userInput == "Y":
			self.RenderQuality = 2

			userInput = input("Human Player[Y/N]:")
			if userInput == "y" or userInput == "Y":
				self.NumberOfBots = 1


			else:
				self.NumberOfBots = 2
			

		else:
			self.RenderQuality = 0
			self.NumberOfBots = 2

		self.WinningMode = False
		if self.NumberOfBots == 1:
			self.WinningMode = True


		if self.RenderQuality == 2:
			import RenderEngine
			self.RenderEngine = RenderEngine.RenderEngine()

		NumberOfThreads = 1
		for loop in range(NumberOfThreads-1):
			Thread(target=self.RunGame, args=("Thread"+str(loop),)).start()
		self.RunGame("main   ")
		return

	def Output(self, numGames, numMoves, timeMoveTook, board, turn):
		if self.RenderQuality == 2:
			text = "Dataset Size: "+str(len(self.AiDataManager.DataSet))+"\n"
			text += "Game: "+str(numGames)+"\n"
			text += "Move: "+str(numMoves)+"\n"
			text += "AVG time: "+str(timeMoveTook)
			self.RenderEngine.UpdateConsoleText(text)

			if board != None and turn != None:
				self.RenderEngine.UpdateBoard(board, turn)
			self.RenderEngine.UpdateFrame()

		if (numMoves % 50 == 0):
			print("done " + str(numMoves) + " moves last took: " + str(timeMoveTook) + " seconds")

		return
	
	def EndOutput(self, numGames, numMoves, timeTaken):
		print("")
		print("Dataset size: " + str(len(self.AiDataManager.DataSet)))
		print("finished game: " + str(numGames+1) + " with " + str(numMoves) + " moves made")
		print("each move took on AVG: " + str((time.time() - timeTaken)/numMoves) + " seconds")
		print("game in total took: " + str(time.time() - timeTaken) + " seconds")
		print("")
		print("")
		return

	def MakeHumanMove(self, game):
		if self.RenderQuality == 2:
			board, turn = self.RenderEngine.MakeHumanMove(game)
		return board, turn

	def RunGame(self, name):
		print("thread started: " + name)
		game = self.Sim.Simulation()
		AIs = []
		for loop in range(2):
			AIs += [AI.BruteForce(self.AiDataManager, winningModeON=self.WinningMode)]
		board, turn = game.Start()

		numGames = 0
		numMoves = 0

		self.Output(numGames, numMoves, 0, board, turn)

		time_taken = time.time()
		MoveTime = time.time()
		while True:
			if self.NumberOfBots >= turn:
				board, turn = MakeAIMove(turn, board, AIs, game)
			else:
				board, turn = self.MakeHumanMove(game)

			numMoves += 1

			Thread(target=self.Output, args=(numGames, numMoves, (time.time() - MoveTime), board, turn,)).start()
			MoveTime = time.time()

			finished, fit = game.CheckFinished()
			if finished == False and numMoves >= 1000:
				finished = True
				fit = [3,3]

			if finished:
				for loop in range(len(AIs)):
					AIs[loop].UpdateData(fit[loop])

				Thread(target=self.EndOutput, args=(numGames, numMoves, time_taken,)).start()

				board, turn = game.Start()
				numGames += 1
				numMoves = 0
				time_taken = time.time()
				MoveTime = time.time()
		return

if __name__ == "__main__":
	RunController()