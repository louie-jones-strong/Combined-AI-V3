import time

def SplitNumber(number):
	output = ""
	number = str(number)
	lenght = len(number)
	if lenght < 4:
		output += str(number)
	else:
		start = lenght % 3
		if start > 0:
			output += str(number[:start]) + ","
		gap = 0
		for loop in range(start, lenght):
			output += str(number[loop])
			gap += 1
			if gap == 3 and loop < lenght-1:
				output += ","
				gap = 0
	return output

def SplitTime(seconds, roundTo=0):
	#Convert seconds to string "[[[DD:]HH:]MM:]SS"
	output = ""
	for scale in 86400, 3600, 60:
		result, seconds = divmod(seconds, scale)
		if output != "" or result > 0:
			if output != "":
				output += ":"
			output += str(int(result))
	if output != "":
		output += ":"
	output += str(round(seconds, roundTo))
	return output

def BytesOutputFormat(numberOfBytes, roundTo=2):
	value  = numberOfBytes
	suffix = "Bytes"

	if numberOfBytes / pow(1024,3) >= 1:
		value  = numberOfBytes/pow(1024,3)
		suffix = "GB"

	elif numberOfBytes / pow(1024,2) >= 1:
		value  = numberOfBytes/pow(1024,2)
		suffix = "MB"

	elif numberOfBytes / 1024 >= 1:
		value  = numberOfBytes/1024
		suffix = "KB"
		

	value = round(value, roundTo)
	return str(value)+" "+suffix

def TimeToDateTime(seconds, dateOn=False, secondsOn=False):
	dateTime = time.gmtime(seconds)
	output = ""
	if dateOn:
		output += str(dateTime.tm_year)+"."+str(dateTime.tm_mon)+"."+str(dateTime.tm_mday)
		output += " : "

	output += str(dateTime.tm_hour)+":"+str(dateTime.tm_min)
	if secondsOn:
		output += ":"+str(dateTime.tm_sec)

	return output
