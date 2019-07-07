import RunController as runner

totalSimsNum = 6

for simNum in range(1, totalSimsNum+1):

	controller = runner.RunController(simNumber=simNum, loadData="N", aiType="b", renderQuality=0, stopTime=60)
	controller.RunTournament()

	controller = runner.RunController(simNumber=simNum, loadData="Y", aiType="b", renderQuality=0, stopTime=60)
	controller.RunTournament()
	
