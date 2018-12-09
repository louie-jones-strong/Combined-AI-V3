from pygame import display,draw,Color
import BruteForce as DraughtsAI
import pygame
import time
import keyboard
import mouse
import math
import draughts

class face(object):
	def __init__(self, points, colour=[255,255,255]):
		self.colour = [colour[0],colour[1],colour[2]]
		self.points = points
		x, y, z = [0,0,0]
		for loop in range(len(points)):
			x += points[loop][0] 
			y += points[loop][1]
			z += points[loop][2]
		x /= len(points)
		y /= len(points)
		z /= len(points)
		self.centre = (x,y,z)

class object3D(object):
	def __init__(self, faces, name="object3D" ,postion3D=[0,0,0], rotation3D=[0,0,0], hidden=False, selected=False):
		self.name = name
		self.postion3D = postion3D
		self.rotation3D = rotation3D
		self.hidden = hidden
		self.selected = selected
		self.faces = faces

def shapes(shape="cube", colour=[255,255,255], stretch=[1,1,1]):
	s=stretch
	if shape == "cube":
		faces= [face([[1*s[0],0*s[1],1*s[2]],[1*s[0],0*s[1],0*s[2]],[1*s[0],1*s[1],0*s[2]],[1*s[0],1*s[1],1*s[2]]]		, colour=colour)]
		faces+=[face([[0*s[0],0*s[1],1*s[2]],[0*s[0],0*s[1],0*s[2]],[0*s[0],1*s[1],0*s[2]],[0*s[0],1*s[1],1*s[2]]]		, colour=colour)]
		faces+=[face([[0*s[0],0*s[1],0*s[2]],[1*s[0],0*s[1],0*s[2]],[1*s[0],1*s[1],0*s[2]],[0*s[0],1*s[1],0*s[2]]]		, colour=colour)]
		faces+=[face([[0*s[0],0*s[1],1*s[2]],[1*s[0],0*s[1],1*s[2]],[1*s[0],0*s[1],0*s[2]],[0*s[0],0*s[1],0*s[2]]]		, colour=colour)]
		faces+=[face([[0*s[0],1*s[1],1*s[2]],[1*s[0],1*s[1],1*s[2]],[1*s[0],1*s[1],0*s[2]],[0*s[0],1*s[1],0*s[2]]]		, colour=colour)]
		faces+=[face([[0*s[0],0*s[1],1*s[2]],[1*s[0],0*s[1],1*s[2]],[1*s[0],1*s[1],1*s[2]],[0*s[0],1*s[1],1*s[2]]]		, colour=colour)]
	elif shape == "face":
		faces= [face([[0*s[0],1*s[1],1*s[2]],[1*s[0],1*s[1],1*s[2]],[1*s[0],1*s[1],0*s[2]],[0*s[0],1*s[1],0*s[2]]]		, colour=colour)]
	return faces
		
class renderEngine(object):
	def rotateX(self, angle, point_3D):
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		y = point_3D[1] * cosa - point_3D[2] * sina
		z = point_3D[1] * sina + point_3D[2] * cosa
		return [point_3D[0], y, z]
	def rotateY(self, angle, point_3D):
		""" Rotates the point around the Y axis by the given angle in degrees. """
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		z = (point_3D[2] * cosa) - (point_3D[0] * sina)
		x = (point_3D[2] * sina) + (point_3D[0] * cosa)

		return [x, point_3D[1], z]
	def rotateZ(self, angle, point_3D):
		""" Rotates the point around the Z axis by the given angle in degrees. """
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		x = point_3D[0] * cosa - point_3D[1] * sina
		y = point_3D[0] * sina + point_3D[1] * cosa
		return [x, y, point_3D[2]]
	def transform(self, point_3D, position3D, rotation3D,globalRotate):
		x = point_3D[0] + position3D[0]
		y = point_3D[1] + position3D[1]
		z = point_3D[2] + position3D[2]

		if globalRotate[0] != 0:
			x,y,z = self.rotateX(globalRotate[0], [x,y,z])
		if globalRotate[1] != 0:
			x,y,z = self.rotateY(globalRotate[1], [x,y,z])
		if globalRotate[2] != 0:
			x,y,z = self.rotateZ(globalRotate[2], [x,y,z])

		return [x,y,z]
	def point3D_to_point2D(self,point_3D):
		x = point_3D[0]
		y = point_3D[1]
		z = point_3D[2]

		factor = self.FOV / (self.viewer_distance + z)
		x = x * factor + self.resolution[0] / 2
		y = -y * factor + self.resolution[1] / 2
		return int(x) , int(y)
	def objects_to_2DFaceList(self,object3D_list,globalRotate):
		face_list = []
		for objectNum in range(len(object3D_list)):#objects
			object3D = object3D_list[objectNum]
			if not object3D.hidden:
				for loop in range(len(object3D.faces)):#faces

					face = []
					for loop2 in range(len(object3D.faces[loop].points)):#points
						point3D = self.transform(object3D.faces[loop].points[loop2], object3D.postion3D, object3D.rotation3D,globalRotate)
						face += [self.point3D_to_point2D(point3D)]

					centre = self.transform(object3D.faces[loop].centre, object3D.postion3D, object3D.rotation3D,globalRotate)

					distance = math.sqrt( centre[0]**2 + centre[1]**2 + (centre[2]-self.FOV)**2 )
					
					face_list += [[ distance , face , object3D.faces[loop].colour , objectNum , object3D.selected ]]

		return sorted(face_list)
	def update_window(self,object3D_list,globalRotate):
		draw.rect(self.window, [0,0,0], [0,0,self.resolution[0],self.resolution[1]], 0)

		face_list = self.objects_to_2DFaceList(object3D_list,globalRotate)

		for loop in range(len(face_list)):

			size = 3

			if self.render_mode[2]:#faces
				pygame.draw.polygon(self.window, face_list[loop][2], face_list[loop][1], 0)	

			if self.render_mode[1]:#lines
				if face_list[loop][4]:
					pygame.draw.polygon(self.window, [255,0,0], face_list[loop][1], size)	
				else:
					pygame.draw.polygon(self.window, [100,100,100], face_list[loop][1], size)

			if self.render_mode[0]:#dots
				for loop2 in range(len(face_list[loop][1])):
					pygame.draw.circle(self.window, [255,255,255], face_list[loop][1][loop2], size)


		if self.FPS != -1:
			label = self.Font.render("FPS:"+str(self.FPS), 1,(255,255,255))
			self.window.blit(label, [10,10])
			label = self.Font.render("Polygons:"+str(len(face_list)), 1,(255,255,255))
			self.window.blit(label, [10,22])
			label = self.Font.render("Objects:"+str(len(object3D_list)), 1,(255,255,255))
			self.window.blit(label, [10,34])
		display.update()
		return
	
	def setup(self):
		display.init()
		pygame.font.init()
		self.resolution = (800,800)
		self.windowPostion = [0,0]
		self.globalRotate = [-45, 0, 0]
		self.FOV = 256
		self.FPS = -1
		self.draging = False
		self.startPos = [0,0]
		self.viewer_distance = 7
		self.rotation_multiplier = 2
		self.render_mode = [False,True,True]
		self.animation = True
		self.PlayAI = True
		self.midMoving = False
		self.Font = pygame.font.SysFont("monospace", 15)
		if False:
			self.resolution = (1920,1080)
			self.window = display.set_mode(self.resolution,pygame.FULLSCREEN )
		else:
			self.window = display.set_mode(self.resolution)

		if self.PlayAI:
			self.animation = False


		temp = mouse.get_position()
		pygame.mouse.set_pos([0,0])
		self.windowPostion = mouse.get_position()
		mouse.move(temp[0], temp[1])

		return
	def setup_object3D_list(self):
		object3D_list = []
		colour1 = [255,255,255]
		colour2 = [0,0,0]
		pickColour = 1
		for loop in range(8):
			for loop2 in range(8):
				pos = [loop-4,-0.5,loop2-4]
				if pickColour == 1:
					object3D_list += [object3D(shapes(shape="face",colour=colour1), name="Board_"+str(loop)+"_"+str(loop2) ,postion3D=pos)]
					pickColour = 2
				else:
					object3D_list += [object3D(shapes(shape="face",colour=colour2), name="Board_"+str(loop)+"_"+str(loop2) ,postion3D=pos)]
					pickColour = 1
			if pickColour == 1:
				pickColour = 2
			else:
				pickColour = 1

		return object3D_list
	def addPieces(self,board):
		object3D_list = []
		for loop in range(8):
			for loop2 in range(8):
				pos = [loop-3.75,0.5,loop2-3.75]
				draw = False
				if board[loop][loop2] == 1 or board[loop][loop2] == 3:
					if board[loop][loop2] == 1:
						shape = shapes(colour=[255,255,255],stretch=[0.5,0.25,0.5])
					else:
						shape = shapes(colour=[255,255,255],stretch=[0.5,0.75,0.5])
					draw = True

				elif board[loop][loop2] == 2 or board[loop][loop2] == 4:
					if board[loop][loop2] == 2:
						shape = shapes(colour=[0,0,0],stretch=[0.5,0.25,0.5])
					else:
						shape = shapes(colour=[0,0,0],stretch=[0.5,0.75,0.5])
					draw = True
					
				if draw:
					object3D_list += [object3D(shape, name="Piece_"+str(loop)+"_"+str(loop2) ,postion3D=pos)]

		return object3D_list
	def moveableAreas(self,board,object3D_list):
		object3D_list[0:63] = self.setup_object3D_list()
		objectNum = 0
		for loop in range(8):
			for loop2 in range(8):
				if board[loop][loop2] == -1:
					object3D_list[objectNum].faces[0].colour = [0,255,0]
				objectNum += 1
		return object3D_list

	def inside_polygon(self,x, y, points):
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
	def getObjectClicked(self,object3D_list,globalRotate):
		pos = mouse.get_position()
		pos = [pos[0]-self.windowPostion[0],pos[1]-self.windowPostion[1]]
		face2DList = self.objects_to_2DFaceList(object3D_list,globalRotate)
		face2DList = face2DList[::-1]

		for loop in range(len(face2DList)):
			if self.inside_polygon(pos[0],pos[1],face2DList[loop][1]):
				return object3D_list[face2DList[loop][3]]
		return None
	def mouseDraging(self):
		if mouse.is_pressed(button="middle") and not self.draging:
			self.startPos = mouse.get_position()
			self.draging = True

		elif not mouse.is_pressed(button="middle") and self.draging:
			change = [0,0]
			finishPos = mouse.get_position()
			change[0] = (self.startPos[1]-finishPos[1])/self.resolution[1]
			change[1] = (self.startPos[0]-finishPos[0])/self.resolution[0]
			self.globalRotate[0] = (self.globalRotate[0] + 360*change[0])%360
			self.globalRotate[1] = (self.globalRotate[1] + 360*change[1])%360 
			self.draging = False

		globalRotate = [self.globalRotate[0],self.globalRotate[1],self.globalRotate[2]]
		if mouse.is_pressed(button="middle") and self.draging:
			change = [0,0]
			finishPos = mouse.get_position()
			change[0] = (self.startPos[1]-finishPos[1])/self.resolution[1]
			change[1] = (self.startPos[0]-finishPos[0])/self.resolution[0]
			globalRotate[0] = (globalRotate[0] + 360*change[0])%360
			globalRotate[1] = (globalRotate[1] + 360*change[1])%360
		return globalRotate

	def __init__(self):
		self.setup()
		FPS_count = 0

		game = draughts.game()
		AI1 = DraughtsAI.Main()
		AI2 = DraughtsAI.Main()
		AI1.Setup(4,8,loadData=False)
		AI2.Setup(4,8,loadData=False)

		board, turn, step = game.start()
		object3D_list = self.setup_object3D_list()
		object3D_list += self.addPieces(board)


		time_taken = time.time()
		while True:		
			if self.animation:
				if turn == 1:  # turn 1
					if self.globalRotate != [-45,0,0]:
						self.globalRotate = [self.globalRotate[0]+(-3),self.globalRotate[1]+(-6),self.globalRotate[2]]
						self.midMoving = True
					else:
						self.globalRotate = [-45,0,0]
						self.midMoving = False

				else: # turn 2
					if self.globalRotate != [45,180,0]:
						self.globalRotate = [self.globalRotate[0]+(3),self.globalRotate[1]+(6),self.globalRotate[2]]
						self.midMoving = True
					else:
						self.globalRotate = [45,180,0]
						self.midMoving = False

				if (self.globalRotate == [0, 90, 0]):
					object3D_list = self.setup_object3D_list()
					object3D_list += self.addPieces(board)

			self.update_window(object3D_list,self.globalRotate)

			if keyboard.is_pressed("esc"):
				display.quit()
				break

			if mouse.is_pressed(button="right") and not self.midMoving and not (self.PlayAI and turn == 2) and False:
				object3D = self.getObjectClicked(object3D_list, self.globalRotate)
				if not object3D == None:
					time.sleep(0.1)
					X = int(object3D.name[6:7])
					Y = int(object3D.name[8:9])

					if object3D.name[0:6] == "Piece_":
						valid, board, step = game.selection(X, Y)
						if step == 2:
							object3D_list[64:-1] = self.addPieces(board)
						if valid:
							object3D.selected = True
							object3D_list = self.moveableAreas(board, object3D_list)

					elif object3D.name[0:6] == "Board_" and step == 2:
						valid, board, turn, step = game.moveCal(X, Y)
						if valid and not self.animation:
							object3D_list = self.setup_object3D_list()
							object3D_list += self.addPieces(board)
			
			elif self.PlayAI and turn == 1:
				print("AI move Turn: " + str(turn))
				valid = False
				while not valid:
					move = AI1.MoveCal(game.FlipBoard())
					valid, board, step = game.selection(move[0], move[1])
					if not valid:
						AI1.UpdateInvalidMove(game.FlipBoard(), move)
					else:
						valid, board, turn, step = game.moveCal(move[2], move[3])
						if not valid:
							AI1.UpdateInvalidMove(game.FlipBoard(), move)

				object3D_list = self.setup_object3D_list()
				object3D_list += self.addPieces(board)

			elif self.PlayAI and turn == 2:
				print("AI move Turn: " + str(turn))
				valid = False
				while not valid:
					move = AI2.MoveCal(board)
					valid, board, step = game.selection(move[0], move[1])
					if not valid:
						AI2.UpdateInvalidMove(board, move)
					else:
						valid, board, turn, step = game.moveCal(move[2], move[3])
						if not valid:
							AI2.UpdateInvalidMove(board, move)

				object3D_list = self.setup_object3D_list()
				object3D_list += self.addPieces(board)

			finished, fit1, fit2 = game.CheckFinished()
			if finished:
				print("finished")
				AI1.UpdateData(fit1)
				AI2.UpdateData(fit2)
				board, turn, step = game.start()


			FPS_count += 1
			if (time.time() - time_taken) >= 0.1:
				self.FPS = FPS_count*10
				FPS_count = 0
				time_taken = time.time()

		return	

if __name__ == "__main__":
	renderEngine()
