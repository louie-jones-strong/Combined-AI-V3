import RunController as runner

sims = [1, 2, 3, 4, 6]

for simNum in sims:

	controller = runner.RunController(simNumber=simNum, loadData="N", aiType="b", renderQuality=0, stopTime=60)
	controller.RunTournament()

	controller = runner.RunController(simNumber=simNum, loadData="Y", aiType="b", renderQuality=0, stopTime=60)
	controller.RunTournament()
	
