
def BoardToKey(board):
	key = str(board)

	#key = serializer(board)
	#key = hash(key)
	return key

def serializer(inputObject):
	outputObject = ""

	if inputObject == None:
		return "None"

	elif type(inputObject) is bytes:
		outputObject = "b("
		for loop in range(len(inputObject)):
			outputObject += str(inputObject[loop])
			if loop < len(inputObject)-1:
				outputObject +=","

		return outputObject + ")"
	
	elif type(inputObject) is str:
		return "'"+inputObject+"'"

	elif hasattr(inputObject, "__len__"):
		outputObject = []
		for loop in range(len(inputObject)):
			outputObject += [serializer(inputObject[loop])]

		outputObject = ",".join(outputObject)
		return "["+outputObject+"]"
	else:
		return str(inputObject)
def deserializer(inputString):

	if inputString.startswith("b("):
		subInputString = inputString[2:-1]
		byteArray = list(map(int, subInputString.split(",")))
		outputObject = bytes(byteArray)

	elif inputString.startswith("["):
		lastIndex = inputString.rfind("]")
		inputString = inputString[1:lastIndex]

		stringList = []
		if inputString.count("[") == 0:
			stringList = inputString.split(",")

		else:
			index = 0
			while index < len(inputString):
				if inputString.startswith(","):
					inputString = inputString[2:]
				index = inputString.find("]")+1
				stringList += [inputString[0:index]]
				inputString = inputString[index:]


		outputObject = list(map(deserializer, stringList))

	elif inputString == "None":
		outputObject = None

	elif inputString == "True":
		outputObject = True

	elif inputString == "False":
		outputObject = False

	elif inputString.startswith("'"):
		outputObject = inputString.replace("'","")

	elif "." in inputString:
		outputObject = float(inputString)

	else:
		try:
		    outputObject = int(inputString)
		except:
		    outputObject = inputString
			
	return outputObject