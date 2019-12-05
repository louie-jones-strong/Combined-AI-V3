from Shared import Logger
import RunController.eRenderType as eRenderType
import RunController.eLoadType as eLoadType
import RunController.RunController as RunController
from Shared import WAndBMetrics
import Shared.AudioManager as AudioManager
import RunController.AgentSetupData as AgentData
import RunController.eAgentType as eAgentType

if __name__ == "__main__":
	AudioManager.sound_setup("Assets//Sounds//Error.wav")
	
	logger = Logger.Logger()
	logger.Clear()

	metricsOn = "T" == input("Metrics On T) Off F)").upper()
	#metricsOn = True
	
	metricsLogger = WAndBMetrics.MetricsLogger("combined-ai-v3", metricsOn)
	
	agentSetupData = []
	agentSetupData += [AgentData.AgentSetupData(eAgentType.eAgentType.Null)]

	try:
		controller = RunController.RunController(logger, 
			metricsLogger, 
			agentSetupData,
			renderQuality=eRenderType.eRenderType.TextOutput, 
			simNumber=None, 
			loadType=eLoadType.eLoadType.Load, 
			stopTime=None)
		
		
		
		controller.RunTraning()

	except Exception as error:
		AudioManager.play_sound()
		logger.LogError(error)
