from pygame import display,draw
import pygame
import time
import keyboard
import math


class game(object):
	def rotateX(self, angle, point_3D):
		""" Rotates the point around the X axis by the given angle in degrees. """
		x = point_3D[0]
		y = point_3D[1]
		z = point_3D[2]
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		y = y * cosa - z * sina
		z = y * sina + z * cosa
		return [x, y, z]
 
	def rotateY(self, angle, point_3D):
		""" Rotates the point around the Y axis by the given angle in degrees. """
		x = point_3D[0]
		y = point_3D[1]
		z = point_3D[2]
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		z = z * cosa - x * sina
		x = z * sina + x * cosa
		return [x, y, z]
 
	def rotateZ(self, angle, point_3D):
		""" Rotates the point around the Z axis by the given angle in degrees. """
		x = point_3D[0]
		y = point_3D[1]
		z = point_3D[2]
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		x = x * cosa - y * sina
		y = x * sina + y * cosa
		return [x, y, z]

	def point3D_to_point2D(self,point_3D):
		x, y, z = point_3D
		factor = self.FOV / (self.viewer_distance + z)
		x = x * factor + self.resolution[0] / 2
		y = -y * factor + self.resolution[1] / 2
		return int(x) , int(y)
		
	def update_window(self,window,faceList,render_mode):
		draw.rect(window, [0,0,0], [0,0,self.resolution[0],self.resolution[1]], 0)

		for loop in range(len(faceList)):
			colour = (255/len(faceList))*(loop+1)

			if render_mode == 0 or render_mode == 2:#render faces or wireframe
				face = []
				for loop2 in range(len(faceList[loop])):
					face += [self.point3D_to_point2D(faceList[loop][loop2])]

				if render_mode == 0:
					pygame.draw.polygon(window, [colour,colour,colour], face, 0)	
				else:
					pygame.draw.polygon(window, [colour,colour,colour], face, 3)	

			elif render_mode == 1:#render points
				for loop2 in range(len(faceList[loop])):
					point = self.point3D_to_point2D(faceList[loop][loop2])
					pygame.draw.circle(window, [colour,colour,colour], point, 3)



		display.update()
		return

	def move_camara_keys_input(self,object_3D):
		#move
		move_vector = [0,0,0]
		if keyboard.is_pressed("w"): 
			move_vector[2] = -1
		elif keyboard.is_pressed("s"): 
			move_vector[2] = 1
		elif keyboard.is_pressed("a"): 
			move_vector[0] = 1
		elif keyboard.is_pressed("d"): 
			move_vector[0] = -1
		elif keyboard.is_pressed("r"): 
			move_vector[1] = -1
		elif keyboard.is_pressed("f"): 
			move_vector[1] = 1


		#rotate
		rotate_vector = [0,0,0]
		if keyboard.is_pressed("up"): 
			rotate_vector[0] = 1
		elif keyboard.is_pressed("down"): 
			rotate_vector[0] = -1
		elif keyboard.is_pressed("left"): 
			rotate_vector[1] = 1
		elif keyboard.is_pressed("right"): 
			rotate_vector[1] = -1

		for loop in range(len(object_3D)):
			for loop2 in range(len(object_3D[loop])):
				
				object_3D[loop][loop2][0] += move_vector[0]*self.movement_multiplier
				object_3D[loop][loop2][1] += move_vector[1]*self.movement_multiplier
				object_3D[loop][loop2][2] += move_vector[2]*self.movement_multiplier
				
				object_3D[loop][loop2] = self.rotateX(rotate_vector[0]*self.rotation_multiplier, object_3D[loop][loop2])
				object_3D[loop][loop2] = self.rotateY(rotate_vector[1]*self.rotation_multiplier, object_3D[loop][loop2])
				object_3D[loop][loop2] = self.rotateZ(rotate_vector[2]*self.rotation_multiplier, object_3D[loop][loop2])





		return object_3D
	
	def main(self):
		self.resolution = (800,800)
		self.FOV = 256
		self.viewer_distance = 4
		self.movement_multiplier = 0.1
		self.rotation_multiplier = 2

		faceList = [
		[[1,-1,1],[1,-1,-1],[1,1,-1],[1,1,1]],#right
		[[-1,-1,1],[-1,-1,-1],[-1,1,-1],[-1,1,1]],#left
		[[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1]],#back
		[[-1,-1,1],[1,-1,1],[1,-1,-1],[-1,-1,-1]],#bottom
		[[-1,1,1],[1,1,1],[1,1,-1],[-1,1,-1]],#top
		[[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]]#front
		]

		display.init()
		window = display.set_mode(self.resolution)
		render_mode = 0
		while True:
			time_taken = time.time()
			faceList = self.move_camara_keys_input(faceList)
			time.sleep(0.01)
			self.update_window(window,faceList,render_mode)

			if keyboard.is_pressed("esc"):
				display.quit()
				break

			elif keyboard.is_pressed("space"):
				time.sleep(0.1)
				render_mode += 1
				if render_mode > 2:
					render_mode = 0

			time_taken = time.time() - time_taken
			time_taken = 1/65-time_taken
			time.sleep(1/65-time_taken)

			print("FPS: " + str(1/time_taken))



game = game()
game.main()