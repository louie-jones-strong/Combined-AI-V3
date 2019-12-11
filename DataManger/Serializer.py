import json

def BoardToKey(board):
	key = str(board)

	#key = serializer(board)
	#key = hash(key)
	return key

def serializer(inputObject):
	# if inputObject == None:
	# 	return "None"

	# inputType = type(inputObject)

	# if inputType is bytes:
	# 	outputObject = "b("
	# 	for loop in range(len(inputObject)):
	# 		outputObject += str(inputObject[loop])
	# 		if loop < len(inputObject)-1:
	# 			outputObject +=","

	# 	return outputObject + ")"
	
	# elif inputType is str:
	# 	return "'"+inputObject+"'"

	# elif hasattr(inputObject, "__len__"):
	# 	outputObject = []
	# 	for loop in range(len(inputObject)):
	# 		outputObject += [serializer(inputObject[loop])]

	# 	outputObject = ",".join(outputObject)
	# 	return "["+outputObject+"]"
	# else:
	# 	return str(inputObject)
	return json.dumps(inputObject)

def deserializer(inputString):

	# if inputString == "None":
	# 	outputObject = None

	# elif inputString == "True":
	# 	outputObject = True

	# elif inputString == "False":
	# 	outputObject = False

	# elif inputString.startswith("b("):
	# 	subInputString = inputString[2:-1]
	# 	byteArray = list(map(int, subInputString.split(",")))
	# 	outputObject = bytes(byteArray)

	# elif inputString.startswith("["):
	# 	lastIndex = inputString.rfind("]")
	# 	inputString = inputString[1:lastIndex]

	# 	stringList = []
	# 	if inputString.count("[") == 0:
	# 		stringList = inputString.split(",")

	# 	else:
	# 		index = 0
	# 		while index < len(inputString):
	# 			if inputString.startswith(","):
	# 				inputString = inputString[2:]
	# 			index = inputString.find("]")+1
	# 			stringList += [inputString[0:index]]
	# 			inputString = inputString[index:]


	# 	outputObject = list(map(deserializer, stringList))

	# elif inputString.startswith("'"):
	# 	outputObject = inputString.replace("'","")

	# elif "." in inputString:
	# 	outputObject = float(inputString)

	# else:
	# 	try:
	# 	    outputObject = int(inputString)
	# 	except:
	# 	    outputObject = inputString
			
	# return outputObject
	return json.loads(inputString)


if __name__ == "__main__":
	import time

	inputObject = [[4,2,3,6,5,3,2,4],
			 [1,1,1,1,1,1,1,1],
			 [0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0],
			 [0,0,0,0,0,0,0,0],
			 [-1,-1,-1,-1,-1,-1,-1,-1],
			 [-4,-2,-3,-6,-5,-3,-2,-4]]

	serializerTime = 0
	deserializerTime = 0

	for loop in range(10000):

		timeMark = time.time()
		serializerOut = serializer(inputObject)
		serializerTime += time.time()-timeMark

		timeMark = time.time()
		deserializer(serializerOut)
		deserializerTime += time.time()-timeMark

	print("Serializer took: "+str(serializerTime))
	print("deserializer took: "+str(deserializerTime))
