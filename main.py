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
	def __init__(self, faces, postion3D=[0,0,0], rotation3D=[0,0,0], hidden=False, selected=True):
		self.postion3D = postion3D
		self.rotation3D = rotation3D
		self.hidden = hidden
		self.faces = faces
		
class game(object):
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
		x,y,z = self.rotateX(rotation3D[0], [x,y,z])
		x,y,z = self.rotateY(rotation3D[1], [x,y,z])
		x,y,z = self.rotateZ(rotation3D[2], [x,y,z])

		x,y,z = self.rotateX(globalRotate[0], [x,y,z])
		x,y,z = self.rotateY(globalRotate[1], [x,y,z])
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
		
	def update_window(self,object3D_list,globalRotate,FPS=0):
		draw.rect(self.window, [0,0,0], [0,0,self.resolution[0],self.resolution[1]], 0)

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
					
					face_list += [[ distance , face , object3D.faces[loop].colour ]]

		face_list = sorted(face_list)

		for loop in range(len(face_list)):
			if self.render_mode[0]:
				for loop2 in range(len(face_list[loop][1])):
					pygame.draw.circle(self.window, [255,255,255], face_list[loop][1][loop2], 3)
					
			if self.render_mode[2]:
				pygame.draw.polygon(self.window, face_list[loop][2], face_list[loop][1], 0)	
			if self.render_mode[1]:
				pygame.draw.polygon(self.window, [100,100,100], face_list[loop][1], 4)	

		if FPS != 0:
			label = self.Font.render("FPS:"+str(FPS), 1,(255,255,255))
			self.window.blit(label, [self.resolution[0]-75,10])
		display.update()
		return

	def move_input(self):
		#rotate
		rotate_vector = [0,0,0]
		#rotate_vector = [1,1,0]
		if keyboard.is_pressed("up"): 
			rotate_vector[0] += 1
		if keyboard.is_pressed("down"): 
			rotate_vector[0] += -1
		if keyboard.is_pressed("left"): 
			rotate_vector[1] += 1
		if keyboard.is_pressed("right"): 
			rotate_vector[1] += -1

		self.globalRotate[0] = (self.globalRotate[0] + rotate_vector[0]*self.rotation_multiplier)%360
		self.globalRotate[1] = (self.globalRotate[1] + rotate_vector[1]*self.rotation_multiplier)%360
		self.globalRotate[2] = (self.globalRotate[2] + rotate_vector[2]*self.rotation_multiplier)%360

		return 
	
	def setup(self):
		display.init()
		pygame.font.init()
		self.Font = pygame.font.SysFont("monospace", 15)
		self.window = display.set_mode(self.resolution)
		self.resolution = (800,800)
		self.globalRotate = [0,0,0]
		self.FOV = 256
		self.viewer_distance = 3
		self.rotation_multiplier = 2
		self.render_mode = [False,True,True]

		object3D_list = []
		object3D_list += [object3D(shapes(),postion3D=[-0.5,-0.5,-0.5])]

		object3D_list[0].faces[0].colour = [255,0,0]
		object3D_list[0].faces[1].colour = [0,255,0]
		object3D_list[0].faces[2].colour = [0,0,255]
		object3D_list[0].faces[3].colour = [255,255,0]
		object3D_list[0].faces[4].colour = [0,255,255]
		object3D_list[0].faces[5].colour = [255,0,255]

		return object3D_list

	def main(self):
		FPS = 0
		FPS_count = 0
		draging = False

		while True:
			time_taken = time.time()
			globalRotate = [self.globalRotate[0],self.globalRotate[1],self.globalRotate[2]]
			if mouse.is_pressed(button='right') and not draging:
				startPos = mouse.get_position()
				draging = True

			elif not mouse.is_pressed(button='right') and draging:
				change = [0,0]
				finishPos = mouse.get_position()
				change[0] = (startPos[1]-finishPos[1])/self.resolution[1]
				change[1] = (startPos[0]-finishPos[0])/self.resolution[0]
				self.globalRotate[0] = (self.globalRotate[0] + 360*change[0])%360
				self.globalRotate[1] = (self.globalRotate[1] + 360*change[1])%360 
				draging = False

			elif mouse.is_pressed(button='right') and draging:
				change = [0,0]
				finishPos = mouse.get_position()
				change[0] = (startPos[1]-finishPos[1])/self.resolution[1]
				change[1] = (startPos[0]-finishPos[0])/self.resolution[0]
				globalRotate[0] = (globalRotate[0] + 360*change[0])%360
				globalRotate[1] = (globalRotate[1] + 360*change[1])%360 

			self.update_window(object3D_list,globalRotate,FPS=FPS)

			if keyboard.is_pressed("esc"):
				display.quit()
				break



			time_taken = time.time() - time_taken
			if time_taken < 1/65:
				time_taken = 1/65-time_taken
				time.sleep(time_taken)

			if FPS_count >= 30:
				FPS = int(1/time_taken)
				FPS_count = 0
			else:
				FPS_count += 1

		return
	
def shapes(shape="cube", colour=[255,255,255]):
	if shape == "cube":
		faces =  [face(	[[1,0,1],[1,0,0],[1,1,0],[1,1,1]]		, colour=colour)]
		faces += [face(	[[0,0,1],[0,0,0],[0,1,0],[0,1,1]]		, colour=colour)]
		faces += [face(	[[0,0,0],[1,0,0],[1,1,0],[0,1,0]]		, colour=colour)]
		faces += [face(	[[0,0,1],[1,0,1],[1,0,0],[0,0,0]]		, colour=colour)]
		faces += [face(	[[0,1,1],[1,1,1],[1,1,0],[0,1,0]]		, colour=colour)]
		faces += [face(	[[0,0,1],[1,0,1],[1,1,1],[0,1,1]]		, colour=colour)]

	return faces

game = game()
game.main()