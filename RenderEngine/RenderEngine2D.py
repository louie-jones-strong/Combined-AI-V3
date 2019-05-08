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
	Resolution = (640, 640)

	def SetNewResolution(self, resolution):
		self.Resolution = resolution
		self.Window = display.set_mode(self.Resolution)
		return

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
		self.LastFrameTook = 0
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

			points = piece.GetRotatedPoints()

			#pygame.draw.polygon(self.Window, fillColor, points, 0)
			#pygame.draw.polygon(self.Window, borderColor, points, 2)

			if piece.Fill and len(points) >= 3:
				pygame.gfxdraw.filled_polygon(self.Window, points, fillColor)
				
			if len(points) >= 3:
				pygame.gfxdraw.aapolygon(self.Window, points, borderColor)
			elif len(points) == 2:
				pygame.gfxdraw.line(self.Window, int(points[0][0]), int(points[0][1]), int(points[1][0]), int(points[1][1]), borderColor)
		return

	def UpdateWindow(self, listBuildTimeTook=0):
		timeMark = time.time()

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
				label = self.Font.render("Last Frame Took:"+str(self.LastFrameTook), 1, (255, 255, 255))
				self.Window.blit(label, [10, 58])

			if self.ConsoleText != "":
				temp = self.ConsoleText.split("\n")
				for loop in range(len(temp)):
					label = self.Font.render(temp[len(temp)-(loop+1)], 1, (255, 255, 255))
					offSet = 22 + loop*12
					self.Window.blit(label, [10, self.Resolution[1]-offSet])

			self.TimeOfLastFrame = time.time()


		display.update()
		listBuildTimeTook += time.time()-timeMark
		self.LastFrameTook = round(listBuildTimeTook, 4)
		return True

	def GetMouseScreenPos(self):
		pos = mouse.get_position()
		x = pos[0]-self.WindowPostion[0]
		y = pos[1]-self.WindowPostion[1]

		x = int(x)
		y = int(y)

		if x < 0 or x > self.Resolution[0] or y < 0 or y > self.Resolution[1]:
			return False, [x, y]
		else:
			return True, [x, y]

	def GetObjectClicked(self):
		if mouse.is_pressed(button="left"):
			inScreenSpace, pos = self.GetMouseScreenPos()

			if inScreenSpace:
				for loop in range(len(self.PieceList)):
					if InsidePolygon(pos, self.PieceList[loop].GetRotatedPoints()):
						return self.PieceList[loop], loop
		return None


if __name__ == "__main__":
	import Shape
	engine = RenderEngine()
	loop = 0
	while True:
		engine.PieceList = [Shape.Piece([350, 350], [100, 100], Shape.Square(), [255,255,255], rotate=loop)]
		loop += 0.1
		if loop >= 360:
			loop = 0

		engine.UpdateWindow()
