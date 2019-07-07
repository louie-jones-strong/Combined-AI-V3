import RunController as runner
from Shared import Logger

sims = [1, 2, 3, 4, 6]

for simNum in sims:

	try:

		controller = runner.RunController(simNumber=simNum, loadData="N", aiType="b", renderQuality=0, stopTime=60)
		controller.RunTournament()

		controller = runner.RunController(simNumber=simNum, loadData="Y", aiType="b", renderQuality=0, stopTime=60)
		controller.RunTournament()

	except Exception as error:
		Logger.LogError(error, holdOnInput=False)
	
