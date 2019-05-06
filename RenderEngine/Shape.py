import math

def BuildCardShapes(pos, scale, suit, value, rotate=0, showFace=True):
	shapes = []

	if showFace:
		shapes += [Piece(pos, scale, CardBackBase(), [255, 255, 255], rotate=rotate)]

		if suit >= 0 and suit <= 3:
			suitPos = RotatePoint([0, 0], rotate, pos)

			if suit == 0:
				shapes += [Piece(suitPos, scale, Circle(), [255, 255, 255], rotate=rotate)]
			elif suit == 1:
				shapes += [Piece(suitPos, scale, Circle(), [255, 255, 255], rotate=rotate)]
			elif suit == 2:
				shapes += [Piece(suitPos, scale, Circle(), [255, 255, 255], rotate=rotate)]
			elif suit == 3:
				shapes += [Piece(suitPos, scale, Circle(), [255, 255, 255], rotate=rotate)]

	else:
		shapes += [Piece(pos, scale, CardBackBase(), [255, 255, 255], rotate=rotate)]

	return shapes

def CardBackBase():
	points = []
	points += [[1, 1]]
	points += [[1, -1]]
	points += [[-1, -1]]
	points += [[-1, 1]]
	return points

def Circle():
	return [[1.0, 0.0], [0.9238795325112867, 0.3826834323650898], 
	[0.7071067811865476, 0.7071067811865476], [0.38268343236508984, 0.9238795325112867], 
	[6.123233995736766e-17, 1.0], [-0.3826834323650897, 0.9238795325112867], 
	[-0.7071067811865475, 0.7071067811865476], [-0.9238795325112867, 0.3826834323650899], 
	[-1.0, 1.2246467991473532e-16], [-0.9238795325112868, -0.38268343236508967], 
	[-0.7071067811865477, -0.7071067811865475], [-0.38268343236509034, -0.9238795325112865], 
	[-1.8369701987210297e-16, -1.0], [0.38268343236509, -0.9238795325112866], 
	[0.7071067811865474, -0.7071067811865477], [0.9238795325112865, -0.3826834323650904]]
	
def Square():
	points = []
	points += [[1, 1]]
	points += [[1, -1]]
	points += [[-1, -1]]
	points += [[-1, 1]]
	return points

def Cross():
	points = []
	points += [[-1, 0.9]]
	points += [[-0.9, 1]]
	points += [[0, 0.1]]
	points += [[0.9, 1]]
	points += [[1, 0.9]]
	points += [[0.1, 0]]
	points += [[1, -0.9]]
	points += [[0.9, -1]]
	points += [[0, -0.1]]
	points += [[-0.9, -1]]
	points += [[-1, -0.9]]
	points += [[-0.1, 0]]
	return points

def Crown():
	points = []
	points += [[-1, -1]]
	points += [[-0.5, -0.5]]
	points += [[0, -1]]
	points += [[0.5, -0.5]]
	points += [[1, -1]]
	points += [[1, 0.5]]
	points += [[-1, 0.5]]
	return points

def HorizontalLine():
	points = []
	points += [[-1, 0.01]]
	points += [[1, 0.01]]
	points += [[-1, -0.01]]
	points += [[1, -0.01]]
	return points
def VerticalLine():
	points = []
	points += [[0.01, -1]]
	points += [[0.01, 1]]
	points += [[-0.01, -1]]
	points += [[-0.01, 1]]
	return points


def RotatePoint(point, degrees, center=[0,0]):
	rotate = degrees*(math.pi/180)  # Convert to radians

	cosValue = math.cos(rotate)
	sinValue = math.sin(rotate)

	rotatedX = cosValue*(point[0]-center[0]) - sinValue*(point[1]-center[1])+center[0]
	rotatedY = sinValue*(point[0]-center[0]) + cosValue*(point[1]-center[1])+center[1]
	return [rotatedX, rotatedY]

class Piece():
	Points = []
	Color = [255, 255, 255]
	Selected = False
	Movable = False
	Fill = True
	InfoObject = None
	Rotate = 0
	Pos = [1,1]
	Scale = [1,1]

	def __init__(self, pos, scale, points, color, fill=True, rotate=0, infoObject=None):
		self.Pos = pos
		self.Scale = scale
		self.Points = points
		self.Color = color
		self.Fill = fill
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
