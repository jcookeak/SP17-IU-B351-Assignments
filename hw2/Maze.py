import re

# ex maze:
# 5	111111
# 4	000100
# 3	100001
# 2	111101
# 1	100001
# 0	110111
#
# 	012345 

#Maze takes a file that contains a maze built from 0's and 1's.
	#provides functions to facilitate searching.
class Maze(object):
	def __init__(self, file):
		#using re for regex to strip newlines lines
		with open(file) as f: #read file and transform maze into array
			self.maze = [x.strip('\n') for x in f.readlines()]
			self.maze.reverse() #reverse list to follow x,y pattern from instructions
		self.entrace = self.find_start()

	#checks if a legal move is on an edge tile and not the start
	def exit(self, x, y):
		if(x == 0 or (x == self.dim()[0]-1) 
			or y == 0 or (y == self.dim()[1]-1)):
			if(self.maze[y][x] == '0' 
				and x != self.entrace[0] and y != self.entrace[1]):
				return True
		return False

	#checks if a move is in bounds and not a wall
	def legal_move(self, x, y):
		# print('testing: ' + str(x) + ',' + str(y))
		if(x<0 or (x > self.dim()[0]-1)):
			# print('fails on x')
			return(False)
		elif(y<0 or (y > self.dim()[1]-1)):
			# print('fails on y')
			return(False)
		elif(self.maze[y][x] == '1'):
			# print('maze val:' + str(self.maze[x][y]))
			# print('fails on maze val')
			return(False)
		else:
			return(True)

	#returns all siblings for a given pair as an array
	#max of four pairs
	def get_sibling(self, x, y):
		sibs = []
		if(self.legal_move(x,y+1)):
			sibs.append((x,y+1))
		if(self.legal_move(x,y-1)):
			sibs.append((x,y-1))
		if(self.legal_move(x+1,y)):
			sibs.append((x+1,y))
		if(self.legal_move(x-1,y)):
			sibs.append((x-1,y))

		return(sibs)

	# returns size of (x,y) dims as a pair
	def dim(self):
		return(len(self.maze[0]), len(self.maze))

	#searches for inital starting point
	#garenteed to be only 1 as explained in lecture
	def find_start(self):
		m = re.compile("[0]")
		for x in m.finditer(self.maze[0]) :
			return((x.start(),0))
		return('error, no start found')

	def find_exits(self, initial):
		exits = []
		visited, stack = [], [initial]
		while stack:
			vertex = stack.pop()
			if vertex not in visited:
				visited.append(vertex)
				if self.exit(vertex[0], vertex[1]):
					exits.append(vertex)
				for x in self.get_sibling(vertex[0],vertex[1]):
					stack.append(x)
		return exits

