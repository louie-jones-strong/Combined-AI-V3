import RunController as runner
from Shared import Logger
import time
from Shared.OutputFormating import SplitTime

Sims = [1, 2, 3, 4, 6]
Agents = ["b"]
hadError = False

for simNum in Sims:
	for agent in Agents:
		print("Setup Sim: "+str(simNum)+" With Agent: "+str(agent))
		input()
		try:
			timeMarkSetup = time.time()
			controller = runner.RunController(simNumber=simNum, loadData="N", aiType=agent, renderQuality=0, stopTime=60)

			print("Setup Done Took: "+SplitTime(time.time()-timeMarkSetup, 2))
			print("Sim = "+str(controller.SimInfo["SimName"]))
			print("Starting Run...")
			input()
			timeMarkRun = time.time()

			controller.RunTournament()
			metaData1 = controller.AiDataManager.MetaData

			controller = runner.RunController(simNumber=simNum, loadData="Y", aiType=agent, renderQuality=0, stopTime=10)
			print("Run Done Took: "+SplitTime(time.time()-timeMarkRun, 2))
			
			metaData2 = controller.AiDataManager.MetaData
			if metaData1 != metaData2:
				Logger.LogWarning("metaData1 != metaData2: save error?", holdOnInput=False)
				hadError = True
			else:
				controller.RunTournament()

		except Exception as error:
			hadError = True
			Logger.LogError(error, holdOnInput=False)


print("test Finished")
if hadError:
	exit(code=1)
	
