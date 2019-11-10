import pickle
import os
from Shared import LoadingBar as LoadingBar
import DataManger.Serializer as Serializer
import threading

def DictAppend(address, dictionary): 
	if (dictionary == {}):
		return

	if (not DictFileExists(address)):
		DictSave(address, dictionary)

	else:
		address += ".txt"
		file = open(address, "a")
		for key, value in dictionary.items():
			file.write(str(key)+":"+Serializer.serializer(value)+"\n")
		file.close()

	return
def DictSave(address, dictionary):
	address += ".txt"
	MakeFolderIfNeeded(address)

	file = open(address, "w")
	for key, value in dictionary.items():
		serializerValue = Serializer.serializer(value)
		file.write(str(key)+":"+serializerValue+"\n")
	file.close()
	return
def DictLoad(address, loadingBar=None):
	dictionary = {}
	address += ".txt"
	file = open(address, "r")
	lines = file.readlines()
	file.close()
	
	numberOfLines = len(lines)
	if loadingBar != None:
		loadingBar.Setup("Loading dict", numberOfLines)

	for loop in range(numberOfLines):
		key, value = lines[loop][:-1].split(":")
		dictionary[key] = Serializer.deserializer(value)

		if loadingBar != None:
			loadingBar.Update(loop)
			
	if loadingBar != None:
		loadingBar.Update(loop)

	return dictionary
def DictFileExists(address):
	return os.path.exists(address+".txt")

def ComplexSave(address, objectInfo):
	address += ".p"
	MakeFolderIfNeeded(address)
	pickle.dump(objectInfo, open(address, "wb"))
	return
def ComplexLoad(address):
	file = open(address+".p", "rb")
	objectInfo = pickle.load(file)
	file.close()
	return objectInfo
def ComplexFileExists(address):
	value = False
	value = os.path.exists(address+".p")
	return value


def MakeFolderIfNeeded(address):
	if "." in address:#has file type
		if "/" not in address:#is at root
			return True
		else:
			folderAddress = address[:address.rfind("//")+2]
	else:
		folderAddress = address

	if not os.path.exists(folderAddress):
		os.makedirs(folderAddress)
		return False
	else:
		return True

class DataSetTable:
	Content = {}
	IsLoaded = False
	Lock = threading.Lock()

	def __init__(self, address, isLoaded):
		self.Lock = threading.Lock()
		self.FileAddress = address
		self.IsLoaded = isLoaded
		self.Content = {}
		return

	def Load(self):
		with self.Lock:
			self.Content = ComplexLoad(self.FileAddress)
			self.IsLoaded = True
		return
	def Save(self):
		with self.Lock:
			ComplexSave(self.FileAddress, self.Content)
		return
	def Unload(self):
		with self.Lock:
			self.Content ={}
			self.IsLoaded = False
		return


class LockAbleObject:
	Lock = threading.Lock()
	Content = {}

	def __init__(self):
		self.Lock = threading.Lock()
		self.Content = {}
		return
