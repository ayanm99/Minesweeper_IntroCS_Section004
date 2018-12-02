import os, random
path = os.getcwd()

class Tile:
	def __init__(self,row,col,value):
		self.row=row
		self.col=col
		self.value=value
		self.status=0 #0 means hidden, 1 means uncovered
		self.img=loadImage(path+"/images/tile.png")

	def checkNeighbours(self,m,n,o):
		return 0<=self.row+m<o and 0<=self.col+n<o  #returns true if there is a neighbour within the board

	def display(self):
		if self.status==0:
			image(self.img,52*self.col,52*self.row,52,52)
		elif self.status==1:
			self.img=loadImage(path+"/images/"+str(self.value)+".png")  #image depends on value and status of tile
			image(self.img,52*self.col,52*self.row,52,52)

class Minesweeper:
	def __init__(self,n,m):
		self.tiles=[]
		self.mines=m
		self.mineCnt=m #to be used in allocating mines
		self.dim=n
		self.game=0		#state of the game. 0=playing, 1=lose,2=win

		for i in range(self.dim):
			for j in range(self.dim):
				t=Tile(i,j,0) #creating tiles without mines
				self.tiles.append(t)
		self.randomMines()
		self.valueAssign()

	def getTiles(self,r,c): #to be used later to retrieve specific tiles from the list
		for i in self.tiles:
			if i.row==r and i.col==c:
				return i


	def randomMines(self):
		r=self.tiles[random.randint(0,(self.dim)**2-1)] #subtract 1 bc list index starts from 0, picks a random element from tiles list
		if r.value!=-1:
			r.value=-1
			self.mineCnt-=1

		if self.mineCnt>=1:
			self.randomMines()  #recursion only runs for mineCnt number of mines
		else:
			return

	def valueAssign(self):
		print("LOL")
		for i in self.tiles:
			if i.value==-1: #only checks tiles with mines
				neighbours=[[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]
				for j in neighbours:
					print(i.row+j[0],i.col+j[1])
					if i.checkNeighbours(j[0],j[1],self.dim)==True and self.getTiles(i.row+j[0],i.col+j[1]).value>-1: #checks if there should be a non-mine element at the neighbouring index
						self.getTiles(i.row+j[0],i.col+j[1]).value+=1 #adds 1 to the value of a tile if its next to a bomb

	def uncoverTiles(self,tile):

		if tile.value==0 and tile.status==0:	#uncovers empty covered tiles
			tile.status=1	#uncovers tile
			neighbours=[[1,1],[-1,0],[1,0],[-1,-1],[0,1],[0,-1],[-1,1],[1,-1]]
			for j in neighbours:
				if tile.checkNeighbours(j[0],j[1],self.dim) and self.getTiles(tile.row+j[0],tile.col+j[1]).value>-1:
					self.uncoverTiles(self.getTiles(tile.row+j[0],tile.col+j[1]))	#recursion makes sure all 0 value tiles are uncovered

		elif tile.value>0 and tile.status==0:
			tile.status=1	#uncovers tile
			numLeft=0
			for i in self.tiles:
				if i.status==0:
					numLeft+=1	#counts number of covered tiles
			
			if numLeft==self.mines:	#wins if all covered tiles are mines
				self.game=2

		elif tile.value==-1:
			tile.status=1
			self.game=1

		else:
			return

	def display(self):
		for i in self.tiles:
			Tile.display(i)
		if self.game==1:
			for i in self.tiles:
				if i.value==-1:
					i.status=1
			img=loadImage(path+"/images/gameover.png")
			image(img,0,0,388//2,314//2)
		if self.game==2:
			for i in self.tiles:
				if i.value==-1:
					i.status=1
			img=loadImage(path+"/images/win.png")
			image(img,0,0,388//2,314//2)

m=Minesweeper(5,3)	#(number of rows & cols, number of mines)

def setup():
	size(52*m.dim,52*m.dim)
	background(255)

def draw():
	m.display()

def mouseClicked():
	i=m.getTiles(mouseY//52,mouseX//52) #//52 because that is the dimension of tiles
	if m.game==0:
		m.uncoverTiles(i)