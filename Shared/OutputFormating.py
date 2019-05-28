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
