import traceback
import time
import Shared.OutputFormating as Format
import os

class Logger:
	MaxLogLines = 1000
	LogsLinesList = []
	OutputAllowed = True
	ClearAllowed = True
	SetTitleAllowed = True
	LoadingBarAllowed = True

	def Clear(self):
		if self.ClearAllowed:
			os.system("cls")
		return

	def SetTitle(self, titleText):
		if self.SetTitleAllowed:
			os.system("title "+str(titleText))
		return
	
	def LogError(self, error, holdOnInput=True):
		if error == None:
			return

		strTrace = traceback.format_exc()

		self.SaveToErrorFile(strTrace.split("\n"), "ERROR")

		if holdOnInput:
			input("Press any Key To contine...")
		return

	def LogWarning(self, warningString, holdOnInput=False):

		self.SaveToErrorFile(warningString.split("\n"), "Warning")

		if holdOnInput:
			input("Press any Key To contine...")
		return

	def Log(self, text):
		print(text)
		self.AddLineToList(text)
		return
	def AddLineToList(self, text):
		self.LogsLinesList += [text]

		if len(self.LogsLinesList) > self.MaxLogLines:
			self.LogsLinesList = self.LogsLinesList[-self.MaxLogLines:]
		return

	def SaveToErrorFile(self, logLines, logType):
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
