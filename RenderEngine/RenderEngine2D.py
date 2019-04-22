from pygame import display,draw,Color,gfxdraw
import pygame
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

		#FPS
		self.FPS = -1
		self.Framecount = 0
		self.LastSampleTime = time.time()
		#vSync
		self.TargetFrameRate = 60
		self.TimeOfLastFrame = 0

		#console text
		self.ConsoleText = ""
		self.MaxNumberOfLines = 6
		return
	def __init__(self):
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)
		display.init()
		pygame.font.init()
		self.SettingSetup()
		self.Running = True

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
		if not self.Running:
			return False


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				self.Running = False
				return False

		if time.time()-self.TimeOfLastFrame >= 1/self.TargetFrameRate:
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

			self.TimeOfLastFrame = time.time()


		display.update()
		return True

	def GetObjectClicked(self):
		if mouse.is_pressed(button="left"):
			pos = mouse.get_position()
			pos = [pos[0]-self.WindowPostion[0],pos[1]-self.WindowPostion[1]]

			for loop in range(len(self.PieceList)):
				if InsidePolygon(pos, self.PieceList[loop].Points):
					return self.PieceList[loop], loop
		return None
