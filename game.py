import pygame
from pygame.locals import *
import time
import copy
import random

from OpenGL.GL import *
from OpenGL.GLU import *


class Axis:
	def __init__(self):
		pass
	def blit(self):
		glBegin(GL_LINES)

		glColor3fv((1,0,0))
		glVertex3fv((0,0,0))
		glVertex3fv((4,0,0))

		glColor3fv((0,1,0))
		glVertex3fv((0,0,0))
		glVertex3fv((0,4,0))

		glColor3fv((0,0,1))
		glVertex3fv((0,0,0))
		glVertex3fv((0,0,4))

		glEnd()

class Object:
	def __init__(self,vertices,edges,surfaces):
		self.vertices = vertices
		self.edges = edges
		self.surfaces = surfaces
	def blit(self):
		edges = self.edges
		vertices = self.vertices
		surfaces = self.surfaces

		
		glBegin(GL_QUADS)
		for surface in surfaces:
			colour = surface[-1]
			for vertex in surface[:-1]:
				glColor3fv(colour)
				glVertex3fv(vertices[vertex])
		glEnd()
		

		glBegin(GL_LINES)
		for edge in edges:
			for vertex in edge:
				glColor3fv((1,1,1))
				glVertex3fv(vertices[vertex])
		glEnd()


	def translatex(self,x):
		vertices = self.vertices
		for point in vertices:
			point[0] = point[0]+x
	def translatey(self,y):
		vertices = self.vertices
		for point in vertices:
			point[1] = point[1]+y
	def translatez(self,z):
		vertices = self.vertices
		for point in vertices:
			point[2] = point[2]+z


class Shooter:
	def __init__(self,vertices,edges,surfaces):
		self.vertices = vertices
		self.edges = edges
		self.surfaces = surfaces
		self.center = None
		self.clock = int(time.time())
		self.rocket1 = None
		self.listrocket = []


	def setCenter(self,center):
		self.center = center
		for vertice in self.vertices:
			vertice[0] = vertice[0] + center[0]
			vertice[1] = vertice[1] + center[1]
			vertice[2] = vertice[2] + center[2]

	def assignRocket1(self,position):
		self.rocket1 = position
		self.rocket1[0] = self.rocket1[0] + self.center[0]
		self.rocket1[1] = self.rocket1[1] + self.center[1]
		self.rocket1[2] = self.rocket1[2] + self.center[2]

	def blit(self):
		curtime = int(time.time())
		if (curtime-self.clock>=1.5):
			if (len(self.listrocket)>0):
				self.listrocket.pop()

		for rocket in self.listrocket:
			for vertex in rocket.vertices:
				vertex[2] = vertex[2] + 1.5
			glBegin(GL_QUADS)
			for surface in rocket.surfaces:
				colour = surface[-1]
				for vertex in surface[:-1]:
					glColor3fv(colour)
					glVertex3fv(rocket.vertices[vertex])
			glEnd()

		edges = self.edges
		vertices = self.vertices
		surfaces = self.surfaces

		for surface in surfaces:
			colour = surface[-1]
			glBegin(GL_POLYGON)
			for vertex in surface[:-1]:
				glColor3fv(colour)
				glVertex3fv(vertices[vertex])
			glEnd()
		
		glBegin(GL_LINES)
		for edge in edges:
			for vertex in edge:
				glColor3fv((0,0,0))
				glVertex3fv(vertices[vertex])
		glEnd()
	
	def shoot(self):
		curtime = int(time.time())
		if (curtime-self.clock>=2):
			p1 = self.rocket1
			x,y = 0.1,0.6
			a1,b1,c1 = p1[0],p1[1],p1[2]
			laser1 = Object(vertices=[[a1-x,b1-x,c1+y],[a1-x,b1+x,c1+y],[a1+x,b1+x,c1+y],[a1+x,b1-x,c1+y],[a1-x,b1-x,c1],[a1-x,b1+x,c1],[a1+x,b1+x,c1],[a1+x,b1-x,c1]],edges=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[4,0],[5,1],[6,2],[7,3]],surfaces=[[0,1,2,3,(1,1,0)],[4,5,6,7,(1,1,0)],[5,1,2,6,(1,1,0)],[4,0,3,7,(1,1,0)],[4,5,1,0,(1,1,0)],[7,6,2,3,(1,1,0)]])
			self.listrocket.append(laser1)
			self.clock = int(time.time())

	def translatex(self,x):
		vertices = self.vertices
		for point in vertices:
			point[0] = point[0]+x
		self.rocket1[0] = self.rocket1[0] + x 
	def translatey(self,y):
		vertices = self.vertices
		for point in vertices:
			point[1] = point[1]+y
		self.rocket1[1] = self.rocket1[1] + y 
	def translatez(self,z):
		vertices = self.vertices
		for point in vertices:
			point[2] = point[2]+z
		self.rocket1[2] = self.rocket1[2] + z 

class Wall:
	def __init__(self,vertices,edges,surfaces,type):
		self.vertices = vertices
		self.edges = edges
		self.surfaces = surfaces
		self.type = type

	def blit(self):
		edges = self.edges
		vertices = self.vertices
		surfaces = self.surfaces
		
		
		for surface in surfaces:
			colour = surface[-1]
			glBegin(GL_POLYGON)
			for vertex in surface[:-1]:
				glColor3fv(colour)
				glVertex3fv(vertices[vertex])
			glEnd()
		
		glBegin(GL_LINES)
		for edge in edges:
			for vertex in edge:
				glColor3fv((1,1,1))
				glVertex3fv(vertices[vertex])
		glEnd()

	def translatex(self,x):
		vertices = self.vertices
		for point in vertices:
			point[0] = point[0]+x
	def translatey(self,y):
		vertices = self.vertices
		for point in vertices:
			point[1] = point[1]+y
	def translatez(self,z):
		vertices = self.vertices
		for point in vertices:
			point[2] = point[2]+z


def collideRocketWall(rocket,incomingwall):
	if len(incomingwall)==0:
		return False
	wall = incomingwall[0]
	rfront = rocket.vertices[0]
	rrear = rocket.vertices[4]
	x,y = rfront[0],rfront[1]
	if wall.type==1:
		if (2<=x<=4 and -3<=y<=5) or (-4<=x<=4 and 1<=y<=5):
			#print("collided")
			if abs(rfront[2]-wall.vertices[0][2])<=1:
				#print("true collided")
				return True
			return False
		return False
	elif wall.type==2:
		if (-4<=x<=4 and 1<=y<=5) or (-4<=x<=-2 and -3<=y<=5):
			#print("collided")
			if abs(rfront[2]-wall.vertices[0][2])<=1:
				#print("true collided")
				return True
			return False
		return False
	elif wall.type==3:
		if (-4<=x<=4 and -3<=y<=1) or (-4<=x<=-2 and -3<=y<=5):
			#print("collided")
			if abs(rfront[2]-wall.vertices[0][2])<=1:
				#print("true collided")
				return True
			return False
		return False
	elif wall.type==4:
		if (-4<=x<=4 and -3<=y<=1) or (2<=x<=4 and -3<=y<=5):
			#print("collided")
			if abs(rfront[2]-wall.vertices[0][2])<=1:
				#print("true collided")
				return True
			return False
		return False
	elif wall.type==5:
		if (-4<=x<=2 and -3<=y<=1):
			#print("collided")
			if abs(rfront[2]-wall.vertices[0][2])<=1:
				#print("true collided")
				return True
			return False
		return False
	elif wall.type==6:
		if (-2<=x<=4 and -3<=y<=1):
			#print("collided")
			if abs(rfront[2]-wall.vertices[0][2])<=1:
				#print("true collided")
				return True
			return False
		return False
	elif wall.type==7:
		if (-2<=x<=4 and 1<=y<=5):
			#print("collided")
			if abs(rfront[2]-wall.vertices[0][2])<=1:
				#print("true collided")
				return True
			return False
		return False
	elif wall.type==8:
		if (-4<=x<=2 and 1<=y<=5):
			#print("collided")
			if abs(rfront[2]-wall.vertices[0][2])<=1:
				#print("true collided")
				return True
			return False
		return False


def collideRocketShooter(rocket,incomingshooter):
	if len(incomingshooter)==0:
		return False
	shooter = incomingshooter[0]
	rfront = rocket.vertices[0]
	rrear = rocket.vertices[4]
	x,y = rfront[0],rfront[1]
	v0,v1,v2,v3 = shooter.vertices[0],shooter.vertices[1],shooter.vertices[2],shooter.vertices[3]
	if (v0[0]<=x<=v1[0] and v1[1]<=y<=v2[1]):
		if abs(rfront[2]-v0[2])<=1.5:
			return True
		return False
	return False


class Plane:
	def __init__(self,vertices,edges,surfaces):
		self.vertices = vertices
		self.edges = edges
		self.surfaces = surfaces
		self.rocket1 = None
		self.rocket2 = None
		self.listrocket = []
		self.clock = int(time.time())
		self.incomingwall = None
		self.incomingshooter = None
		self.score = 0


	def linkWall(self,incomingwall):
		self.incomingwall = incomingwall

	def linkShooter(self,incomingshooter):
		self.incomingshooter = incomingshooter

	def assignRocket1(self,position):
		self.rocket1 = position

	def assignRocket2(self,position):
		self.rocket2 = position

	def collideBulletPlane(self):
		if len(self.incomingshooter)==0:
			return False
		shooter = self.incomingshooter[0]
		if len(shooter.listrocket)==0:
			return False
		pfront = self.vertices[5]
		prear = self.vertices[10]
		ptop = self.vertices[12]
		pbottom = self.vertices[24]
		pleft = self.vertices[8]
		pright = self.vertices[2]

		for bullet in shooter.listrocket:
			if bullet.vertices[0][2]>=pfront[2] and bullet.vertices[0][2]<=prear[2]:
				if (bullet.vertices[0][1]<=ptop[1] and bullet.vertices[0][1]>=pbottom[1]) and (bullet.vertices[0][0]>=pleft[0] and bullet.vertices[0][0]<=pright[0]):
					return True
		return False

	def collidePlaneWall(self):
		if len(self.incomingwall)==0:
			return False
		wall = self.incomingwall[0]
		pfront = self.vertices[5]
		prear = self.vertices[10]
		ptop = self.vertices[12]
		pbottom = self.vertices[24]
		pleft = self.vertices[8]
		pright = self.vertices[2]
		if wall.type==1:
			if pfront[2]<=wall.vertices[0][2] and prear[2]>=wall.vertices[0][2]:
				if (ptop[1]<=1 and pbottom[1]>=-3) and (pleft[0]>=-4 and pright[0]<=2):
					return False
				return True
			return False
		elif wall.type==2:
			if pfront[2]<=wall.vertices[0][2] and prear[2]>=wall.vertices[0][2]:
				if (ptop[1]<=1 and pbottom[1]>=-3) and (pleft[0]>=-2 and pright[0]<=4):
					return False
				return True
			return False
		elif wall.type==3:
			if pfront[2]<=wall.vertices[0][2] and prear[2]>=wall.vertices[0][2]:
				if (ptop[1]<=5 and pbottom[1]>=1) and (pleft[0]>=-2 and pright[0]<=4):
					return False
				return True
			return False
		elif wall.type==4:
			if pfront[2]<=wall.vertices[0][2] and prear[2]>=wall.vertices[0][2]:
				if (ptop[1]<=5 and pbottom[1]>=1) and (pleft[0]>=-4 and pright[0]<=2):
					return False
				return True
			return False
		elif wall.type==5:
			if pfront[2]<=wall.vertices[0][2] and prear[2]>=wall.vertices[0][2]:
				if (ptop[1]<=5 and pbottom[1]>=1) and (pleft[0]>=-4 and pright[0]<=4):
					return False
				return True
			return False
		elif wall.type==6:
			if pfront[2]<=wall.vertices[0][2] and prear[2]>=wall.vertices[0][2]:
				if (ptop[1]<=5 and pbottom[1]>=1) and (pleft[0]>=-4 and pright[0]<=4):
					return False
				return True
			return False
		elif wall.type==7:
			if pfront[2]<=wall.vertices[0][2] and prear[2]>=wall.vertices[0][2]:
				if (ptop[1]<=1 and pbottom[1]>=-3) and (pleft[0]>=-4 and pright[0]<=4):
					return False
				return True
			return False
		elif wall.type==8:
			if pfront[2]<=wall.vertices[0][2] and prear[2]>=wall.vertices[0][2]:
				if (ptop[1]<=1 and pbottom[1]>=-3) and (pleft[0]>=-4 and pright[0]<=4):
					return False
				return True
			return False

	def blit(self):
		curtime = int(time.time())
		if (curtime-self.clock>=2):
			if (len(self.listrocket)>0):
				self.listrocket.pop()
				if (len(self.listrocket)>0):
					self.listrocket.pop()


		rocketpoplist = []
		for rocket in self.listrocket:
			if collideRocketWall(rocket,self.incomingwall):
				rocketpoplist.append(rocket)
			if collideRocketShooter(rocket,self.incomingshooter):
				self.score+=1
				rocketpoplist.append(rocket)
				self.incomingshooter.pop()
			for vertex in rocket.vertices:
				vertex[2] = vertex[2] - 1.5
			glBegin(GL_QUADS)
			for surface in rocket.surfaces:
				colour = surface[-1]
				for vertex in surface[:-1]:
					glColor3fv(colour)
					glVertex3fv(rocket.vertices[vertex])
			glEnd()

		for rocket in rocketpoplist:
			if rocket in self.listrocket:
				self.listrocket.remove(rocket)

		edges = self.edges
		vertices = self.vertices
		surfaces = self.surfaces
		
		for surface in surfaces:
			colour = surface[-1]
			glBegin(GL_POLYGON)
			for vertex in surface[:-1]:
				glColor3fv(colour)
				glVertex3fv(vertices[vertex])
			glEnd()
		
		glBegin(GL_LINES)
		for edge in edges:
			for vertex in edge:
				glColor3fv((0,0,0))
				glVertex3fv(vertices[vertex])
		glEnd()

	def translatex(self,x):
		self.rocket1[0] = self.rocket1[0] + x
		self.rocket2[0] = self.rocket2[0] + x
		vertices = self.vertices
		for point in vertices:
			point[0] = point[0]+x
	def translatey(self,y):
		self.rocket1[1] = self.rocket1[1] + y
		self.rocket2[1] = self.rocket2[1] + y
		vertices = self.vertices
		for point in vertices:
			point[1] = point[1]+y
	def translatez(self,z):
		self.rocket1[2] = self.rocket1[2] + z
		self.rocket2[2] = self.rocket2[2] + z
		vertices = self.vertices
		for point in vertices:
			point[2] = point[2]+z

	def shoot(self):
		curtime = int(time.time())
		if (curtime-self.clock>=1.5):
			p1 = self.rocket1
			x,y = 0.1,0.6
			a1,b1,c1 = p1[0],p1[1],p1[2]
			p2 = self.rocket2
			a2,b2,c2 = p2[0],p2[1],p2[2]
			laser1 = Object(vertices=[[a1-x,b1-x,c1+y],[a1-x,b1+x,c1+y],[a1+x,b1+x,c1+y],[a1+x,b1-x,c1+y],[a1-x,b1-x,c1],[a1-x,b1+x,c1],[a1+x,b1+x,c1],[a1+x,b1-x,c1]],edges=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[4,0],[5,1],[6,2],[7,3]],surfaces=[[0,1,2,3,(1,1,0)],[4,5,6,7,(1,1,0)],[5,1,2,6,(1,1,0)],[4,0,3,7,(1,1,0)],[4,5,1,0,(1,1,0)],[7,6,2,3,(1,1,0)]])
			laser2 = Object(vertices=[[a2-x,b2-x,c2+y],[a2-x,b2+x,c2+y],[a2+x,b2+x,c2+y],[a2+x,b2-x,c2+y],[a2-x,b2-x,c2],[a2-x,b2+x,c2],[a2+x,b2+x,c2],[a2+x,b2-x,c2]],edges=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[4,0],[5,1],[6,2],[7,3]],surfaces=[[0,1,2,3,(1,1,0)],[4,5,6,7,(1,1,0)],[5,1,2,6,(1,1,0)],[4,0,3,7,(1,1,0)],[4,5,1,0,(1,1,0)],[7,6,2,3,(1,1,0)]])
			self.listrocket.append(laser1)
			self.listrocket.append(laser2)
			self.clock = int(time.time())

higschore = [0]

def scoreFunc():
	pygame.init()
	display = (600,600)
	win = pygame.display.set_mode(display)
	pygame.display.set_caption("High Score")

	font = pygame.font.Font('freesansbold.ttf',20)
	text1 = font.render("your High Score:- "+str(higschore[0]),True,(255,255,0),(0,0,0))
	text2 = font.render("Play Again",True,(0,255,0),(0,0,0))
	text3 = font.render("Quit",True,(255,0,0),(0,0,0))
	text4 = font.render("Info",True,(255,255,255),(0,0,0))


	message1 = font.render("Move with a-w-s-d, destroy as many bots coming forward to",True,(255,255,255),(0,0,255))
	message2 = font.render("collect points and dogde from their bullet attacks. Avoid the",True,(255,255,255),(0,0,255))
	message3 = font.render("walls coming forward by flying in through the open space",True,(255,255,255),(0,0,255))

	text1Rect = text1.get_rect()
	text2Rect = text2.get_rect()
	text3Rect = text3.get_rect()
	text4Rect = text4.get_rect()
	message1Rect = message1.get_rect()
	message2Rect = message2.get_rect()
	message3Rect = message3.get_rect()
	text1Rect.center = (300,150)
	text2Rect.center = (300,300)
	text3Rect.center = (300,350)
	text4Rect.center = (300,400)
	message1Rect.center = (300,450)
	message2Rect.center = (300,500)
	message3Rect.center = (300,550)

	run = True
	while run:
		pygame.time.delay(10)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				x,y = event.pos
				if (text3Rect.collidepoint(x,y)):
					print("quit")
					run = False
				elif (text2Rect.collidepoint(x,y)):
					print("play again")
					run = False
					main()

		win.fill((0,0,0))
		win.blit(text1,text1Rect)
		win.blit(text2,text2Rect)
		win.blit(text3,text3Rect)
		win.blit(text4,text4Rect)
		win.blit(message1,message1Rect)
		win.blit(message2,message2Rect)
		win.blit(message3,message3Rect)
		pygame.display.update()

	pygame.quit()

def main():

	axis = Axis()
	leftwall = Object(vertices=[[-4,-3,10],[-4,-3,-100],[-4,5,-100],[-4,5,10]],edges=[[0,1],[1,2],[2,3],[3,0]],surfaces=[[0,1,2,3,(0.7,0.7,0.7)]])
	rightwall = Object(vertices=[[4,-3,10],[4,-3,-100],[4,5,-100],[4,5,10]],edges=[[0,1],[1,2],[2,3],[3,0]],surfaces=[[0,1,2,3,(0.7,0.7,0.7)]])
	downwall = Object(vertices=[[-4,-3,10],[-4,-3,-100],[4,-3,-100],[4,-3,10]],edges=[[0,1],[1,2],[2,3],[3,0]],surfaces=[[0,1,2,3,(0.3,0.3,0.3)]])

	plane = Plane(vertices=[[1/2.5,0,0],[5/2.5,-1/2/2.5,0],[5/2.5,-1/2/2.5,-1/2.5],[1/2.5,0,-2/2.5],[2/3/2.5,0,-4/2.5],[0,0,-5/2.5],[-2/3/2.5,0,-4/2.5],[-1/2.5,0,-2/2.5],[-5/2.5,-1/2/2.5,-1/2.5],[-5/2.5,-1/2/2.5,0],[-1/2.5,0,0],[-1/2.5,0,-11/6/2.5],[-3/2.5,2/2.5,-11/6/2.5],[-3/2.5,2/2.5,-1/6/2.5],[-1/2.5,0,-1/6/2.5],[1/2.5,0,-11/6/2.5],[3/2.5,2/2.5,-11/6/2.5],[3/2.5,2/2.5,-1/6/2.5],[1/2.5,0,-1/6/2.5],[-1/2.5,0,0],[-1/2/2.5,1/2/2.5,0],[1/2/2.5,1/2/2.5,0],[1/2.5,0,0],[1/2/2.5,-1/2/2.5,0],[-1/2/2.5,-1/2/2.5,0],[-1/3.5,0,0.01],[-1/2/3.5,1/2/3.5,0.01],[1/2/3.5,1/2/3.5,0.01],[1/3.5,0,0.01],[1/2/3.5,-1/2/3.5,0.01],[-1/2/3.5,-1/2/3.5,0.01],[0,0,-3/2.5],[1/2/2.5,0,-7/2/2.5],[0,0,-4/2.5],[-1/2/2.5,0,-7/2/2.5],[1/4/2.5,1/2/2.5,-7/2/2.5],[-1/4/2.5,1/2/2.5,-7/2/2.5]],edges=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,0],[11,12],[12,13],[13,14],[14,11],[15,16],[16,17],[17,18],[18,15],[19,20],[20,21],[21,22],[22,23],[23,24],[24,19],[31,32],[32,33],[33,34],[34,31],[31,35],[35,33],[31,36],[36,33],[32,35],[35,36],[36,34]],surfaces=[[0,1,2,3,(1/3,1/3,1/3)],[7,8,9,10,(1/3,1/3,1/3)],[0,3,7,10,(1/4,1/4,1/4)],[3,4,5,6,7,(2/3,2/3,2/3)],[11,12,13,14,(3/255,81/255,19/255)],[15,16,17,18,(3/255,81/255,19/255)],[19,20,21,22,23,24,(252/255,34/255,10/255)],[25,26,27,28,29,30,(255/255,231/255,3/255)],[31,32,35,(67/255,120/255,226/255)],[31,35,36,(67/255,120/255,226/255)],[31,36,34,(67/255,120/255,226/255)],[33,32,35,(67/255,120/255,226/255)],[33,35,36,(67/255,120/255,226/255)],[33,36,34,(67/255,120/255,226/255)]])
	plane.assignRocket1([-3/2.5,-1/4/2.5,-3/2/2.5])
	plane.assignRocket2([3/2.5,-1/4/2.5,-3/2/2.5])


	shooter1 = Shooter(vertices=[[-1,0,1],[1,0,1],[1,2,1],[-1,2,1],[-1,0,-1],[1,0,-1],[1,2,-1],[-1,2,-1],[-0.5,0.5,1.1],[0.5,0.5,1.1],[0.5,3/2,1.1],[-0.5,3/2,1.1],[-1/4,3/4,1.2],[1/4,3/4,1.2],[1/4,5/4,1.2],[-1/4,5/4,1.2]],edges=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7],[8,9],[9,10],[10,11],[11,9],[12,13],[13,14],[14,15],[15,12]],surfaces=[[0,1,2,3,(1/3,1/3,1/3)],[4,5,6,7,(1/3,1/3,1/3)],[0,1,5,4,(1/3,1/3,1/3)],[3,2,6,7,(1/3,1/3,1/3)],[1,2,6,5,(1/3,1/3,1/3)],[0,3,7,4,(1/3,1/3,1/3)],[8,9,10,11,(1,0,0)],[12,13,14,15,(1/3,1/3,1/3)]])


	wall1 = Wall(vertices=[[4,5,-100],[4,-3,-100],[2,-3,-100],[2,1,-100],[-4,1,-100],[-4,5,-100]],edges=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]],surfaces=[[0,1,2,3,4,5,(102/255,10/255,182/255)]],type=1)
	wall2 = Wall(vertices=[[-4,5,-100],[-4,-3,-100],[-2,-3,-100],[-2,1,-100],[4,1,-100],[4,5,-100]],edges=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]],surfaces=[[0,1,2,3,4,5,(102/255,10/255,182/255)]],type=2)
	wall3 = Wall(vertices=[[-4,-3,-100],[-4,5,-100],[-2,5,-100],[-2,1,-100],[4,1,-100],[4,-3,-100]],edges=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]],surfaces=[[0,1,2,3,4,5,(102/255,10/255,182/255)]],type=3)
	wall4 = Wall(vertices=[[4,-3,-100],[4,5,-100],[2,5,-100],[2,1,-100],[-4,1,-100],[-4,-3,-100]],edges=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]],surfaces=[[0,1,2,3,4,5,(102/255,10/255,182/255)]],type=4)
	wall5 = Wall(vertices=[[-4,-3,-100],[-4,1,-100],[2,1,-100],[2,-3,-100]],edges=[[0,1],[1,2],[2,3],[3,0]],surfaces=[[0,1,2,3,(102/255,10/255,182/255)]],type=5)
	wall6 = Wall(vertices=[[-2,-3,-100],[-2,1,-100],[4,1,-100],[4,-3,-100]],edges=[[0,1],[1,2],[2,3],[3,0]],surfaces=[[0,1,2,3,(102/255,10/255,182/255)]],type=6)
	wall7 = Wall(vertices=[[-2,1,-100],[-2,5,-100],[4,5,-100],[4,1,-100]],edges=[[0,1],[1,2],[2,3],[3,0]],surfaces=[[0,1,2,3,(102/255,10/255,182/255)]],type=7)
	wall8 = Wall(vertices=[[-4,1,-100],[-4,5,-100],[2,5,-100],[2,1,-100]],edges=[[0,1],[1,2],[2,3],[3,0]],surfaces=[[0,1,2,3,(102/255,10/255,182/255)]],type=8)
	wallList = [wall1,wall2,wall3,wall4,wall5,wall6,wall7,wall8]
	shooterList = [shooter1]
	incomingwall=[copy.deepcopy(wallList[random.randint(0,7)])]
	incomingshooter = []
	plane.linkWall(incomingwall)
	plane.linkShooter(incomingshooter)

	pygame.init()
	display = (900,500)
	win = pygame.display.set_mode(display,DOUBLEBUF|OPENGL)
	pygame.display.set_caption("Speed Way Run")
	gluPerspective(45,(display[0]/display[1]),0.1,120.0)
	glTranslatef(0,-1,-5)
	glEnable(GL_DEPTH_TEST)

	run = True
	while run:
		pygame.time.delay(10)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]:
			left = plane.vertices[8]
			if left[0]-0.07>-4:
				plane.translatex(-0.07)
				glTranslatef(0.07,0,0)
		if keys[pygame.K_d]:
			right = plane.vertices[2]
			if right[0]+0.07<4:
				plane.translatex(0.07)
				glTranslatef(-0.07,0,0)
		if keys[pygame.K_w]:
			top = plane.vertices[12]
			if top[1]+0.07<5:
				plane.translatey(0.07)
				glTranslatef(0,-0.07,0)

		if keys[pygame.K_s]:
			bottom = plane.vertices[9]
			if bottom[1]-0.07>-3:
				plane.translatey(-0.07)
				glTranslatef(0,0.07,0)

		if keys[pygame.K_SPACE]:
			plane.shoot()

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		wall = incomingwall[0]
		
		if wall.vertices[0][2]<4:
			wall.blit()
			wall.translatez(0.5)
			if len(incomingshooter)>0:
				shooter = incomingshooter[0]
				shooter.blit()
				shooter.translatez(0.5)
				shooter.shoot()
		else:
			wall = copy.deepcopy(wallList[random.randint(0,7)])
			incomingwall[0] = wall

			shooter = copy.deepcopy(shooterList[0])
			if wall.type==1:
				shooter.setCenter([-3,-3,-99])
				shooter.assignRocket1([0,1,1])

			elif wall.type==2:
				shooter.setCenter([3,-3,-99])
				shooter.assignRocket1([0,1,1])

			elif wall.type==3:
				shooter.setCenter([3,3,-99])
				shooter.assignRocket1([0,1,1])

			elif wall.type==4:
				shooter.setCenter([-3,3,-99])
				shooter.assignRocket1([0,1,1])

			elif wall.type==5:
				a,b,c = [3,-3,-99], [3,3,-99], [-3,3,-99]
				temp = [a,b,c]
				shooter.setCenter(temp[random.randint(0,2)])
				shooter.assignRocket1([0,1,1])

			elif wall.type==6:
				a,b,c = [-3,-3,-99], [3,3,-99], [-3,3,-99]
				temp = [a,b,c]
				shooter.setCenter(temp[random.randint(0,2)])
				shooter.assignRocket1([0,1,1])

			elif wall.type==7:
				a,b,c = [-3,-3,-99], [3,-3,-99], [-3,3,-99]
				temp = [a,b,c]
				shooter.setCenter(temp[random.randint(0,2)])
				shooter.assignRocket1([0,1,1])

			elif wall.type==8:
				a,b,c = [-3,-3,-99], [3,-3,-99], [3,3,-99]
				temp = [a,b,c]
				shooter.setCenter(temp[random.randint(0,2)])
				shooter.assignRocket1([0,1,1])

			if len(incomingshooter)==0:
				incomingshooter.append(shooter)
			else:
				incomingshooter[0] = shooter

		leftwall.blit()
		rightwall.blit()
		downwall.blit()
		plane.blit()
		if (plane.collidePlaneWall() or plane.collideBulletPlane()):
			run = False
		pygame.display.flip()
	print("you're score:- "+str(plane.score))
	higschore[0] = plane.score
	scoreFunc()
main()
