import RenderEngine.PolygonPiece as Piece
from RenderEngine.PieceBase import RotatePoint as RotatePoint

def BuildCardShapes(pos, scale, suit, value, rotate=0, showFace=True):
	shapes = []
	
	shapes += [Piece.PolygonPiece(pos, scale, CardBackBase(), [255, 255, 255], rotate=rotate)]
	if showFace:

		if suit >= 0 and suit <= 3:
			if suit == 0:
				suitPiece = Diamonds()
				suitColour = [255, 0, 0]
			elif suit == 1:
				suitPiece = Clubs()
				suitColour = [0, 0, 0]
			elif suit == 2:
				suitPiece = Hearts()
				suitColour = [255, 0, 0]
			elif suit == 3:
				suitPiece = Spades()
				suitColour = [0, 0, 0]
			
			suitScale = [scale[0]*0.1, scale[1]*0.1]

			tempPos = RotatePoint([pos[0]+scale[0]*0.55, pos[1]+scale[1]*0.75], rotate, pos)
			shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

			tempPos = RotatePoint([pos[0]-scale[0]*0.55, pos[1]-scale[1]*0.75], rotate, pos)
			shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

			if value == 0:
				suitScale = [scale[0]*0.5, scale[1]*0.5]
				tempPos = RotatePoint(pos, rotate, pos)
				shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

			elif value == 10:
				suitScale = [scale[0]*0.5, scale[1]*0.5]
				tempPos = RotatePoint(pos, rotate, pos)
				shapes += [Piece.PolygonPiece(tempPos, suitScale, Jack(), suitColour, rotate=rotate)]

			elif value == 11:
				suitScale = [scale[0]*0.5, scale[1]*0.5]
				tempPos = RotatePoint(pos, rotate, pos)
				shapes += [Piece.PolygonPiece(tempPos, suitScale, Queen(), suitColour, rotate=rotate)]

			elif value == 12:
				suitScale = [scale[0]*0.5, scale[1]*0.5]
				tempPos = RotatePoint(pos, rotate, pos)
				shapes += [Piece.PolygonPiece(tempPos, suitScale, Crown(), suitColour, rotate=rotate)]

			else:
			
				suitScale = [scale[0]*0.1, scale[1]*0.1]
				if value == 1 or value == 2:
					tempPos = RotatePoint([pos[0], pos[1]+scale[0]*0.45], rotate, pos)
					shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

					tempPos = RotatePoint([pos[0], pos[1]-scale[0]*0.45], rotate, pos)
					shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

				if value == 2 or value == 4 or value == 8:
					tempPos = RotatePoint(pos, rotate, pos)
					shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

				if value >= 5 and 7 >= value:
					tempPos = RotatePoint([pos[0]+scale[0]*0.3, pos[1]], rotate, pos)
					shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

					tempPos = RotatePoint([pos[0]-scale[0]*0.3, pos[1]], rotate, pos)
					shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

				if value >= 3 and 9 >= value:
					tempPos = RotatePoint([pos[0]+scale[0]*0.3, pos[1]+scale[0]*0.45], rotate, pos)
					shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

					tempPos = RotatePoint([pos[0]+scale[0]*0.3, pos[1]-scale[0]*0.45], rotate, pos)
					shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

					tempPos = RotatePoint([pos[0]-scale[0]*0.3, pos[1]+scale[0]*0.45], rotate, pos)
					shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

					tempPos = RotatePoint([pos[0]-scale[0]*0.3, pos[1]-scale[0]*0.45], rotate, pos)
					shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

					if value >= 5 and 7 >= value:
						tempPos = RotatePoint([pos[0]+scale[0]*0.3, pos[1]], rotate, pos)
						shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

						tempPos = RotatePoint([pos[0]-scale[0]*0.3, pos[1]], rotate, pos)
						shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

						if value == 6 or value == 7:
							tempPos = RotatePoint([pos[0], pos[1]-scale[0]*0.3], rotate, pos)
							shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]
		
							if value == 7:
								tempPos = RotatePoint([pos[0], pos[1]+scale[0]*0.3], rotate, pos)
								shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

					elif value == 8 or value == 9:
						tempPos = RotatePoint([pos[0]+scale[0]*0.15, pos[1]+scale[0]*0.25], rotate, pos)
						shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

						tempPos = RotatePoint([pos[0]+scale[0]*0.15, pos[1]-scale[0]*0.25], rotate, pos)
						shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

						tempPos = RotatePoint([pos[0]-scale[0]*0.15, pos[1]+scale[0]*0.25], rotate, pos)
						shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

						tempPos = RotatePoint([pos[0]-scale[0]*0.15, pos[1]-scale[0]*0.25], rotate, pos)
						shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

						if value == 9:
							tempPos = RotatePoint([pos[0], pos[1]-scale[0]*0.4], rotate, pos)
							shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]

							tempPos = RotatePoint([pos[0], pos[1]+scale[0]*0.4], rotate, pos)
							shapes += [Piece.PolygonPiece(tempPos, suitScale, suitPiece, suitColour, rotate=rotate)]
			

	return shapes

def CardBackBase():
	return [[-0.4983, -0.9863], [0.3952, -1.0], 
	[0.5326, -0.9863], [0.6495, -0.9244], [0.6838, 0.7663], 
	[0.6564, 0.9038], [0.5533, 0.9794], [-0.5052, 1.0], 
	[-0.5945, 0.9588], [-0.6495, 0.8694], [-0.6838, -0.8351], [-0.622, -0.945]]

def Diamonds():
	return [[-0.1207, -1.0], [0.6379, -0.046], 
	[-0.0517, 1.0], [-0.6379, 0.0]]
def Clubs():
	return [[0.0479, -1.0], [0.7577, -0.1606], 
	[0.7972, 0.2394], [0.6507, 0.4535], [0.3634, 0.5211], 
	[0.0704, 0.1155], [0.1549, 0.8423], [0.4761, 0.9944], 
	[-0.2789, 1.0], [0.0423, 0.8479], [-0.0085, 0.1268], 
	[-0.3521, 0.5606], [-0.6563, 0.5268], 
	[-0.7972, 0.2507], [-0.7352, -0.1493]]
def Hearts():
	return [[-0.1055, -0.407], [0.2462, -0.8191], 
	[0.6884, -0.9296], [0.9799, -0.6583], [1.0, -0.2362], 
	[-0.0854, 0.9296], [-0.9397, -0.1859], [-1.0, -0.6583], 
	[-0.7085, -0.9196], [-0.2965, -0.7186]]
def Spades():
	return [[-0.1667, -0.9494], [0.1548, -0.9613], 
	[0.3869, -0.7113], [0.4048, -0.3482], [0.2262, -0.0982], 
	[0.5179, -0.1815], [0.8393, -0.1815], [1.0, -0.0149], 
	[1.0, 0.3423], [0.8452, 0.5089], [0.506, 0.4792], 
	[0.2679, 0.2827], [0.1131, 0.2827], [0.125, 0.8065], 
	[0.3988, 0.9554], [-0.2321, 0.9613], [-0.006, 0.8065], 
	[-0.0119, 0.3006], [-0.1964, 0.3006], [-0.4643, 0.4613], 
	[-0.8155, 0.4792], [-0.994, 0.3542], [-1.0, 0.003], 
	[-0.869, -0.1101], [-0.506, -0.1161], [-0.25, -0.0268], 
	[-0.4583, -0.2887], [-0.4762, -0.6756]]

def Jack():
	return [[-0.9789, -0.986], [0.986, -1.0], 
	[0.986, -0.7193], [0.2702, -0.7404], [0.2912, 0.3053], 
	[0.2561, 0.6842], [0.1439, 0.8526], [-0.2, 1.0], 
	[-0.6912, 1.0], [-0.9789, 0.7614], [-0.8246, 0.5649], 
	[-0.6211, 0.7544], [-0.2842, 0.7684], [0.0035, 0.6772], 
	[0.0526, 0.5719], [0.0386, -0.7333], [-0.986, -0.7404]]
def Queen():
	return [[-0.2063, -1.0], [0.2381, -0.9111], 
	[0.5238, -0.619], [0.6381, -0.0032], [0.4984, 0.5429], 
	[0.7778, 0.7905], [0.6825, 1.0], [0.4095, 0.746], 
	[0.2254, 0.9492], [-0.1429, 0.9937], [-0.5365, 0.8603], 
	[-0.6508, 0.6063], [-0.7397, 0.219], [-0.7778, -0.346], 
	[-0.6127, -0.8095], [-0.4349, -0.6317], [-0.5492, -0.2698], 
	[-0.5111, 0.219], [-0.4159, 0.6254], [-0.1937, 0.7397], 
	[0.1111, 0.7143], [0.219, 0.6254], [0.0286, 0.4286], 
	[0.1492, 0.2952], [0.3206, 0.4603], [0.454, -0.0032], 
	[0.3587, -0.5619], [0.1429, -0.7206], [-0.1746, -0.746], 
	[-0.4413, -0.6381], [-0.6063, -0.8032]]

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
