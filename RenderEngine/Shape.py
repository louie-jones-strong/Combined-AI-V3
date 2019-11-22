import RenderEngine.Piece.PolygonPiece as Piece
from RenderEngine.Piece.PieceBase import RotatePoint as RotatePoint

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
