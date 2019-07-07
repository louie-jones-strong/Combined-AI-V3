import RunController as runner
from Shared import Logger

sims = [1, 2, 3, 4, 6]
hadError = False

for simNum in sims:

	try:

		controller = runner.RunController(simNumber=simNum, loadData="N", aiType="b", renderQuality=0, stopTime=60)
		controller.RunTournament()

		controller = runner.RunController(simNumber=simNum, loadData="Y", aiType="b", renderQuality=0, stopTime=60)
		controller.RunTournament()

	except Exception as error:
		hadError = True
		Logger.LogError(error, holdOnInput=False)

if hadError:
	exit(code=1)
	
