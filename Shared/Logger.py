import traceback
import time
import Shared.OutputFormating as Format

def LogError(error):
	if error == None:
		return



	strTrace = traceback.format_exc()

	OutputLog(strTrace.split("\n"), "ERROR")

	input("Press any Key To contine...")
	return

def OutputLog(logLines, logType):
	if logLines[-1] == "\n" or logLines[-1] == "":
		logLines = logLines[:len(logLines)-1]

	outputLines = ["========================================================="]
	outputLines += ["IME:"+Format.TimeToDateTime(time.time(),True, True)+" LOGTYPE:"+str(logType)]
	outputLines += [""]
	outputLines += logLines
	outputLines += [""]
	outputLines += ["========================================================="]

	for line in outputLines:
		print(line)


	return outputLines