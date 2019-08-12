import RunController as runner
from Shared import Logger
import time
from Shared.OutputFormating import SplitTime
from DataManger import BasicLoadAndSave

class Tests:
	MetaDataAddress = "Logs//TestOutputs//"

	def __init__(self):
		self.Logger = Logger.Logger()
		self.Logger.ClearAllowed = False
		self.Logger.SetTitleAllowed = False
		self.Logger.LoadingBarAllowed = False
		self.Logger.InputAllowed = False

		Sims = [1, 2, 3, 4, 6]
		Agents = ["b"]

		hadError = False

		timeMark = time.time()
		for simNum in Sims:
			for agent in Agents:
				if self.RunTest(simNum, agent):
					hadError = True

		print("Full Test Took: "+SplitTime(time.time()-timeMark))

		print("tests Finished")

		if hadError:
			exit(code=1)
		return


	def RunTest(self, simNum, agent):
		hadError = False
		print("")
		print("Setup Sim: "+str(simNum)+" With Agent: "+str(agent))

		try:
			timeMarkSetup = time.time()
			controller = runner.RunController(self.Logger, simNumber=simNum, loadData="N", aiType=agent, renderQuality=0, trainNetwork="Y", stopTime=60)

			print("Setup Done Took: "+SplitTime(time.time()-timeMarkSetup))
			print("Sim = "+controller.SimInfo["SimName"])
			print("Starting Run...")
			timeMarkRun = time.time()

			controller.RunTournament()
			metaData1 = controller.AiDataManager.MetaData.Content

			address = self.MetaDataAddress+"MetaData_" +controller.SimInfo["SimName"]+"_"+agent+"_1"
			BasicLoadAndSave.DictSave(address, metaData1)

			print("Run+Save Took: "+SplitTime(time.time()-timeMarkRun))
			print("Games Played: " + str(metaData1["NumberOfGames"]))
			print("Moves Played: " + str(metaData1["MovesPlayed"]))
			print("dataset size: " + str(metaData1["SizeOfDataSet"]))
			print("number complete boards: " + str(metaData1["NumberOfCompleteBoards"]))
			print("number finished boards: " + str(metaData1["NumberOfFinishedBoards"]))

			controller = runner.RunController(self.Logger, simNumber=simNum, loadData="Y", aiType=agent, renderQuality=0, trainNetwork="N", stopTime=10)

			metaData2 = controller.AiDataManager.MetaData.Content
			address = self.MetaDataAddress+"MetaData_" + controller.SimInfo["SimName"]+"_"+agent+"_2"
			BasicLoadAndSave.DictSave(address, metaData2)

			metaDataSame = True
			for key in metaData1.keys():
				if key not in metaData2 or metaData1[key] != metaData2[key]:
					metaDataSame = False
					break

			if not metaDataSame:
				self.Logger.LogWarning("sim: "+controller.SimInfo["SimName"]+" AI: " +agent+" metaData1 != metaData2: save error?")
				hadError = True
			else:
				controller.RunTournament()

		except Exception as error:
			hadError = True
			self.Logger.LogError(error)

		return hadError


if __name__ == "__main__":
	Tests()
