import RunController as runner
from Shared import Logger

sims = [1, 2, 3, 4, 6]
hadError = False

for simNum in sims:

	try:

		controller = runner.RunController(simNumber=simNum, loadData="N", aiType="b", renderQuality=0, stopTime=60)
		controller.RunTournament()
		metaData1 = controller.AiDataManager.MetaData["SizeOfDataSet"]

		controller = runner.RunController(simNumber=simNum, loadData="Y", aiType="b", renderQuality=0, stopTime=60)
		
		metaData2 = controller.AiDataManager.MetaData["SizeOfDataSet"]
		if metaData1 != metaData2:
			Logger.LogWarning("metaData1 != metaData2: save error?", holdOnInput=False)
			hadError = True

		controller.RunTournament()

	except Exception as error:
		hadError = True
		Logger.LogError(error, holdOnInput=False)

if hadError:
	exit(code=1)
	
