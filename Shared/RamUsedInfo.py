import sys


def GetFullSizeOf(inputObject):
	size = sys.getsizeof(inputObject)
	
	if type(inputObject) is dict:
		for key, value in inputObject.items():
			size += GetFullSizeOf(key)
			size += GetFullSizeOf(value)

	elif (hasattr(inputObject, "__len__") and 
		type(inputObject) is not str):

		for loop in range(len(inputObject)):
			size += GetFullSizeOf(inputObject[loop])

	return size


