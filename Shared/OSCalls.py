import os

def ClearShell():
	if 0 != os.system("cls"):
		os.system("clear")
	return

def SetTitle(titleText):
	os.system("title "+str(titleText))
	return