import BruteForce as AI
import importlib
import time
import os
import sys
import keyboard
from threading import Thread

def MakeAIMove(turn, board, AIs, game):
	AI = AIs[turn-1]
	valid = False
	if turn == 1:
		while not valid:
			move = AI.MoveCal(game.FlipBoard(board))
			flipedMove = game.FlipInput(move)
			valid, board, turn = game.MakeMove(flipedMove)
			if not valid:
				AI.UpdateInvalidMove(game.FlipBoard(board), move)
		
	else:
		while not valid:
			move = AI.MoveCal(board)
			valid, board, turn = game.MakeMove(move)
			if not valid:
				AI.UpdateInvalidMove(board, move)
	return board, turn

def SplitNumber(number):
	output = ""
	number = str(number)
	lenght = len(number)
	if lenght < 4:
		output += str(number)
	else:
		start = lenght % 3
		if start > 0:
			output += str(number[:start]) + ","
		gap = 0
		for loop in range(start, lenght):
			output += str(number[loop])
			gap += 1
			if gap == 3 and loop < lenght-1:
				output += ","
				gap = 0
	return output

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

		self.SimInfo = self.Sim.Simulation().Info
		if userInput == "n" or userInput == "N":
			self.AiDataManager = AI.DataSetManager(self.SimInfo["NumInputs"], self.SimInfo["MinInputSize"], self.SimInfo["MaxInputSize"], self.SimInfo["Resolution"], datasetAddress, loadData=False)

		else:
			self.AiDataManager = AI.DataSetManager(self.SimInfo["NumInputs"], self.SimInfo["MinInputSize"], self.SimInfo["MaxInputSize"], self.SimInfo["Resolution"], datasetAddress, loadData=True)

		#setting 
		self.RenderQuality = int(input("Render level[0][1][2]: "))
		self.NumberOfBots = self.SimInfo["MaxPlayers"]
		self.LastOutputTime = time.time()

		if self.RenderQuality != 0:

			userInput = input("Human Player[Y/N]:")
			if userInput == "y" or userInput == "Y":
				self.NumberOfBots -= 1


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

	def Output(self, game, numGames, numMoves, gameStartTime, totalStartTime, board, turn, finished=False):
		numGames += 1
		avgMoveTime = 0
		if numMoves != 0:
			avgMoveTime = (time.time() - gameStartTime)/numMoves
			avgMoveTime = round(avgMoveTime,6)
		
		if self.RenderQuality == 2:
			text = "Dataset Size: "+str(len(self.AiDataManager.DataSet))+"\n"
			text += "Game: "+str(numGames)+"\n"
			text += "Move: "+str(numMoves)+"\n"
			text += "AVG time: "+str(avgMoveTime)
			self.RenderEngine.UpdateConsoleText(text)

			if board != None and turn != None:
				self.RenderEngine.UpdateBoard(board, turn)
			self.RenderEngine.UpdateFrame()

		if (time.time() - self.LastOutputTime) >= 1:
			if self.RenderQuality == 1 and self.NumberOfBots >= turn:
				os.system("cls")
				game.SimpleOutput(board)

			print("Dataset size: " + str(SplitNumber(len(self.AiDataManager.DataSet))))
			print("Number Of Complete Boards: " + str(SplitNumber(self.AiDataManager.NumberOfCompleteBoards)))
			if finished:
				print("game: " + str(SplitNumber(numGames)) + " move: " + str(SplitNumber(numMoves)) + " finished game")
			else:
				print("game: " + str(SplitNumber(numGames)) + " move: " + str(SplitNumber(numMoves)))
			print("moves avg took: " + str(avgMoveTime) + " seconds")
			print("Games avg took: " + str( round((time.time() - totalStartTime)/(numGames),6)) + " seconds")
			print("time since start: " + str(round(time.time() - totalStartTime, 2)) + " seconds")
			
			self.LastOutputTime = time.time()
		return
	
	def MakeHumanMove(self, game, board):
		if self.RenderQuality == 1:

			valid = False
			while not valid:
				os.system("cls")
				game.SimpleOutput(board)
				move = []

				for loop in range(self.SimInfo["NumInputs"]):
					validMove = False

					while not validMove:
						userInput = float(input("input["+ str(loop) +"]: "))
						userInput = self.SimInfo["Resolution"] * round(float(userInput)/self.SimInfo["Resolution"])
						print(userInput)

						if userInput >= self.SimInfo["MinInputSize"] and userInput <= self.SimInfo["MaxInputSize"]:
							validMove = True
							move += [userInput]
						else:
							print("not in the range!")

				valid, board, turn = game.MakeMove(move)
				if not valid:
					print("that move was not vaild")
						
			print("")
			game.SimpleOutput(board)
		
		elif self.RenderQuality == 2:
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

		totalStartTime = time.time()
		gameStartTime = time.time()
		lastSaveTime = time.time()
		while True:
			if self.NumberOfBots >= turn:
				board, turn = MakeAIMove(turn, board, AIs, game)
			else:
				board, turn = self.MakeHumanMove(game, board)

			numMoves += 1

			self.Output(game, numGames, numMoves, gameStartTime, totalStartTime, board, turn)

			if keyboard.is_pressed("esc"):
				break

			finished, fit = game.CheckFinished()
			if finished:

				if time.time() - lastSaveTime > 5:
					for loop in range(len(AIs)):
						AIs[loop].UpdateData(fit[loop])
					lastSaveTime = time.time()

				self.Output(game, numGames, numMoves, gameStartTime, totalStartTime, board, turn, finished=True)

				board, turn = game.Start()
				numGames += 1
				numMoves = 0
				gameStartTime = time.time()

		return

if __name__ == "__main__":
	RunController()