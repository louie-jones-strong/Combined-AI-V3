import sys
import os


def GetFullSizeOf(inputObject):
	size = sys.getsizeof(inputObject)
	

	return size


def GetFolderSize(folder):
	totalSize = os.path.getsize(folder)

	for item in os.listdir(folder):
		itemPath = os.path.join(folder, item)

		if os.path.isfile(itemPath):
			totalSize += os.path.getsize(itemPath)

		elif os.path.isdir(itemPath):
			totalSize += GetFolderSize(itemPath)

	return totalSize

