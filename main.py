from pygame import display,draw,Color
import pygame
import time
import keyboard
import mouse
import math

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
	def __init__(self, faces, postion3D=[0,0,0], rotation3D=[0,0,0], hidden=False, selected=False):
		self.postion3D = postion3D
		self.rotation3D = rotation3D
		self.hidden = hidden
		self.selected = selected
		self.faces = faces

def shapes(shape="cube", colour=[255,255,255]):
	if shape == "cube":
		faces =  [face(	[[1,0,1],[1,0,0],[1,1,0],[1,1,1]]		, colour=colour)]
		faces += [face(	[[0,0,1],[0,0,0],[0,1,0],[0,1,1]]		, colour=colour)]
		faces += [face(	[[0,0,0],[1,0,0],[1,1,0],[0,1,0]]		, colour=colour)]
		faces += [face(	[[0,0,1],[1,0,1],[1,0,0],[0,0,0]]		, colour=colour)]
		faces += [face(	[[0,1,1],[1,1,1],[1,1,0],[0,1,0]]		, colour=colour)]
		faces += [face(	[[0,0,1],[1,0,1],[1,1,1],[0,1,1]]		, colour=colour)]

	return faces
		
class renderEngine(object):
	def rotateX(self, angle, point_3D):
		""" Rotates the point around the X axis by the given angle in degrees. """
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
		for objectNum in range(len(object3D_list)):
			object3D = object3D_list[objectNum]
			if not object3D.hidden:
				for loop in range(len(object3D.faces)):

					face = []
					for loop2 in range(len(object3D.faces[loop].points)):
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
			if self.render_mode[0]:
				for loop2 in range(len(face_list[loop][1])):
					pygame.draw.circle(self.window, [255,255,255], face_list[loop][1][loop2], 3)
					
			if self.render_mode[2]:
				pygame.draw.polygon(self.window, face_list[loop][2], face_list[loop][1], 0)	
			if self.render_mode[1]:
				if face_list[loop][4]:
					pygame.draw.polygon(self.window, [255,0,0], face_list[loop][1], 4)	
				else:
					pygame.draw.polygon(self.window, [100,100,100], face_list[loop][1], 4)	

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
		self.globalRotate = [0,0,0]
		self.FOV = 256
		self.FPS = -1
		self.draging = False
		self.startPos = [0,0]
		self.viewer_distance = 3
		self.rotation_multiplier = 2
		self.render_mode = [False,True,True]
		self.Font = pygame.font.SysFont("monospace", 15)
		if False:
			self.resolution = (1920,1080)
			self.window = display.set_mode(self.resolution,pygame.FULLSCREEN )
		else:
			self.window = display.set_mode(self.resolution)

		temp = mouse.get_position()
		pygame.mouse.set_pos([0,0])
		self.windowPostion = mouse.get_position()
		mouse.move(temp[0], temp[1])

		return
	def setup_object3D_list(self):
		object3D_list = []
		for loop in range(1):
			object3D_list += [object3D(shapes(),postion3D=[-0.5,-0.5,-0.5])]

		for loop in range(len(object3D_list)):
			object3D_list[loop].faces[0].colour = [255,0,0]
			object3D_list[loop].faces[1].colour = [0,255,0]
			object3D_list[loop].faces[2].colour = [0,0,255]
			object3D_list[loop].faces[3].colour = [255,255,0]
			object3D_list[loop].faces[4].colour = [0,255,255]
			object3D_list[loop].faces[5].colour = [255,0,255]
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
		for loop in range(len(face2DList)):
			if self.inside_polygon(pos[0],pos[1],face2DList[loop][1]):
				return object3D_list[face2DList[loop][3]]
		return None
	def mouseDraging(self):
		if mouse.is_pressed(button='middle') and not self.draging:
			self.startPos = mouse.get_position()
			self.draging = True

		elif not mouse.is_pressed(button='middle') and self.draging:
			change = [0,0]
			finishPos = mouse.get_position()
			change[0] = (self.startPos[1]-finishPos[1])/self.resolution[1]
			change[1] = (self.startPos[0]-finishPos[0])/self.resolution[0]
			self.globalRotate[0] = (self.globalRotate[0] + 360*change[0])%360
			self.globalRotate[1] = (self.globalRotate[1] + 360*change[1])%360 
			self.draging = False

		globalRotate = [self.globalRotate[0],self.globalRotate[1],self.globalRotate[2]]
		if mouse.is_pressed(button='middle') and self.draging:
			change = [0,0]
			finishPos = mouse.get_position()
			change[0] = (self.startPos[1]-finishPos[1])/self.resolution[1]
			change[1] = (self.startPos[0]-finishPos[0])/self.resolution[0]
			globalRotate[0] = (globalRotate[0] + 360*change[0])%360
			globalRotate[1] = (globalRotate[1] + 360*change[1])%360
		return globalRotate

	def __init__(self):
		self.setup()
		object3D_list = self.setup_object3D_list()
		FPS = 0
		FPS_count = 0

		time_taken = time.time()
		while True:
			globalRotate = self.mouseDraging()

			self.update_window(object3D_list,globalRotate)

			if keyboard.is_pressed("esc"):
				display.quit()
				break


			FPS_count += 1
			if (time.time() - time_taken) >= 0.1:
				self.FPS = FPS_count*10
				FPS_count = 0
				time_taken = time.time()

		return
	
if __name__ == "__main__":
	renderEngine()