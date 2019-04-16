import math

def Circle():
	n = 4
	r = 1
	return [(math.cos(2*math.pi/n*x)*r, math.sin(2*math.pi/n*x)*r) for x in range(0, n)]
def Square():
	points = []
	points += [[1, 1]]
	points += [[1, -1]]
	points += [[-1, -1]]
	points += [[-1, 1]]
	return points

class Piece():
	Points = []
	Color = [255, 255, 255]
	Selected = False
	Movable = False

	def __init__(self, pos, scale, points):
		for loop in range(len(points)):
			points[loop][0] *= scale[0]
			points[loop][1] *= scale[1]
			
			points[loop][0] += pos[0]
			points[loop][1] += pos[1]

		self.Points = points
		return