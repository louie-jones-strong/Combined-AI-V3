from pygame import display,draw,Color,gfxdraw
import pygame
import Shape
import time
import mouse
import math
import os

def InsidePolygon(pos2D, points):
	x = pos2D[0]
	y = pos2D[1]

	n = len(points)
	inside = False
	p1x, p1y = points[0]
	for i in range(1, n + 1):
		p2x, p2y = points[i % n]
		if y > min(p1y, p2y):
			if y <= max(p1y, p2y):
				if x <= max(p1x, p2x):
					if p1y != p2y:
						xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
					if p1x == p2x or x <= xinters:
						inside = not inside
		p1x, p1y = p2x, p2y
	return inside

class RenderEngine:
	ConsoleText = ""
	PieceList = []
	Resolution = (700, 700)

	def SettingSetup(self):
		#window
		self.Font = pygame.font.SysFont("monospace", 15)
		self.Window = display.set_mode(self.Resolution)

		#================
		temp = mouse.get_position()
		pygame.mouse.set_pos([0, 0])
		self.WindowPostion = mouse.get_position()
		mouse.move(temp[0], temp[1])
		self.startPos = [0, 0]

		#highlighting
		self.HighlightFadeTime = 2
		

		#FPS
		self.FPS = -1
		self.Framecount = 0
		self.LastSampleTime = time.time()

		#console text
		self.ConsoleText = ""
		self.MaxNumberOfLines = 6
		return
	def __init__(self):
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)
		display.init()
		pygame.font.init()
		self.SettingSetup()

		self.PieceList = []

		return
	def DrawPieces(self):
		for loop in range(len(self.PieceList)):
			piece = self.PieceList[loop]

			if (piece.Movable):
				fillColor = [0, 255, 0]
			else:
				fillColor = piece.Color

			if (piece.Selected):
				borderColor = [255, 0, 0]
			else:
				borderColor = [0, 0, 0]


			#pygame.draw.polygon(self.Window, fillColor, piece.Points, 0)
			#pygame.draw.polygon(self.Window, borderColor, piece.Points, 2)

			pygame.gfxdraw.filled_polygon(self.Window, piece.Points, fillColor)
			pygame.gfxdraw.aapolygon(self.Window, piece.Points, borderColor)

		return

	def UpdateWindow(self):
		draw.rect(self.Window, [50, 50, 50], [0, 0, self.Resolution[0], self.Resolution[1]], 0)
		self.DrawPieces()



		#text on the screen
		self.Framecount += 1
		if (time.time() - self.LastSampleTime) >= 0.1:
			self.FPS = self.Framecount*10
			self.Framecount = 0
			self.LastSampleTime = time.time()

		if self.FPS != -1:
			label = self.Font.render("FPS:"+str(self.FPS), 1, (255, 255, 255))
			self.Window.blit(label, [10, 10])
			label = self.Font.render("Objects:"+str(len(self.PieceList)), 1, (255, 255, 255))
			self.Window.blit(label, [10, 34])

		if self.ConsoleText != "":
			temp = self.ConsoleText.split("\n")
			for loop in range(len(temp)):
				label = self.Font.render(temp[len(temp)-(loop+1)], 1, (255, 255, 255))
				offSet = 22 + loop*12
				self.Window.blit(label, [10, self.Resolution[1]-offSet])

		display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
		return

	def GetObjectClicked(self):
		if mouse.is_pressed(button="left"):
			pos = mouse.get_position()
			pos = [pos[0]-self.WindowPostion[0],pos[1]-self.WindowPostion[1]]

			for loop in range(len(self.PieceList)):
				if InsidePolygon(pos, self.PieceList[loop].Points):
					return self.PieceList[loop], loop
		return None


def getgrid():
	pieceSize = 30
	PieceList = []
	boardColor = True
	grid = [8,8]
	for x in range(grid[0]):
		for y in range(grid[1]):

			if boardColor:
				color = [255,255,255]
				boardColor = False
			else:
				color = [0,0,0]
				boardColor = True

			PieceList += [Shape.Piece([((x+0.5)-grid[0]/2)*pieceSize*2+350, ((y+0.5)-grid[1]/2)*pieceSize*2+350], [pieceSize, pieceSize], Shape.Square(), color)]
		
		if boardColor:
			boardColor = False
		else:
			boardColor = True
	return PieceList
def getPiece():
	pieceSize = 20
	gridSize = 30
	board = [[1, 0, 1, 0, 0, 0, 2, 0], 
			[0, 1, 0, 0, 0, 2, 0, 2], 
			[1, 0, 1, 0, 0, 0, 2, 0], 
			[0, 1, 0, 0, 0, 2, 0, 2], 
			[1, 0, 1, 0, 0, 0, 2, 0], 
			[0, 1, 0, 0, 0, 2, 0, 2], 
			[1, 0, 1, 0, 0, 0, 2, 0], 
			[0, 1, 0, 0, 0, 2, 0, 2]]

	PieceList = []
	grid = [8,8]
	for x in range(grid[0]):
		for y in range(grid[1]):
			if board[x][y] != 0:
				if board[x][y] == 1:
					PieceList += [Shape.Piece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)*gridSize*2+350], [pieceSize, pieceSize], Shape.Circle(), [255,255,255])]
				else:
					PieceList += [Shape.Piece([((x+0.5)-grid[0]/2)*gridSize*2+350, ((y+0.5)-grid[1]/2)*gridSize*2+350], [pieceSize, pieceSize], Shape.Circle(), [0,0,0])]
	return PieceList

if __name__ == "__main__":
	grid = getgrid()

	temp = True
	engine = RenderEngine()
	loop= 0
	while True:
		engine.PieceList = []
		engine.PieceList += grid
		engine.PieceList += getPiece()

		if temp:
			engine.PieceList += [Shape.Piece([350, 350], [loop/10, loop/10], Shape.Square(), [255,0,0])]
		else:
			engine.PieceList += [Shape.Piece([350, 350], [loop/10, loop/10], Shape.Square(), [0,0,255])]

		if loop == 250:
			if temp:
				temp = False
			else:
				temp = True
			loop = 0

		engine.UpdateWindow()
		loop += 1
