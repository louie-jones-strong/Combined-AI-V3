from pygame import display,draw,Color
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

class RenderEngine(object):
	ConsoleText = ""
	PieceList = []

	def SettingSetup(self):
		#window
		self.resolution = (700, 700)
		self.Font = pygame.font.SysFont("monospace", 15)
		self.Window = display.set_mode(self.resolution)

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

	def DrawBackGround(self):

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


			pygame.draw.polygon(self.Window, fillColor, piece.Points, 0)
			pygame.draw.polygon(self.Window, borderColor, piece.Points, 5)

		return

	def UpdateWindow(self):
		draw.rect(self.Window, [0, 0, 0], [0, 0, self.resolution[0], self.resolution[1]], 0)
		self.DrawBackGround()
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
				self.Window.blit(label, [10, self.resolution[1]-offSet])

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


if __name__ == "__main__":
	engine = RenderEngine()
	loop= 0
	while True:
		engine.PieceList = [Shape.Piece([350, 350], [loop/10, loop/10], Shape.Square())]
		if (loop > 3500):
			loop = 0
		engine.UpdateWindow()
		loop += 1
