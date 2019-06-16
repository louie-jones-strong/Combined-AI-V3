import traceback
import time
import Shared.OutputFormating as Format
import os

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
	outputLines += ["TIME:"+Format.TimeToDateTime(time.time(),True, True)+" LOGTYPE:"+str(logType)]
	outputLines += [""]
	outputLines += logLines
	outputLines += [""]
	outputLines += ["========================================================="]

	output = "\n".join(outputLines)
	print(output)	

	address = "Logs//"
	if not os.path.exists(address):
		os.makedirs(address)

	address += "ErrorLog.txt"

	if not os.path.exists(address):
		file = open(address, "w")
	else:
		file = open(address, "a")
	file.write(output)
	file.close()


	return outputLines