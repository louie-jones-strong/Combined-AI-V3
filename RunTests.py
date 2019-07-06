import RunController as runner

controller = runner.RunController(simNumber=6, loadData="N", aiType="r", renderQuality=0, stopTime=60)
controller.RunTournament()