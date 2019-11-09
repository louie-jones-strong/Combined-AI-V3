import math

def RotatePoint(point, degrees, center=[0, 0]):
	rotate = degrees*(math.pi/180)  # Convert to radians

	cosValue = math.cos(rotate)
	sinValue = math.sin(rotate)

	rotatedX = cosValue*(point[0]-center[0]) - sinValue * \
            (point[1]-center[1])+center[0]
	rotatedY = sinValue*(point[0]-center[0]) + cosValue * \
            (point[1]-center[1])+center[1]
	return [rotatedX, rotatedY]


class PieceBase():
	def __init__(self, pos, scale, points, rotate=0, infoObject=None):
		self.Pos = pos
		self.Scale = scale
		self.Points = points
		self.Rotate = rotate
		self.InfoObject = infoObject
		return

	def GetRotatedPoints(self):
		rotatedPoints = []

		for loop in range(len(self.Points)):
			point = self.Points[loop]
			point = RotatePoint(point, self.Rotate)

			point[0] *= self.Scale[0]
			point[1] *= self.Scale[1]

			point[0] += self.Pos[0]
			point[1] += self.Pos[1]

			rotatedPoints += [point]

		return rotatedPoints

	def Draw(self, window):

		return
