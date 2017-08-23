from Maze import * #import custome class Maze

# applies a dfs until an exit slot is found
def search(Maze, initial):
	visited, stack = [], [initial]
	while stack:
		vertex = stack.pop()
		if vertex not in visited:
			visited.append(vertex) 
			#checks if node is an exit, 
			#if so return path taken upto this point
			if Maze.exit(vertex[0], vertex[1]): 
				#return both true and the path taken
				return(True, visited)
			#get all neighboring nodes to continue seaching for an exit
			for x in Maze.get_sibling(vertex[0],vertex[1]):
				stack.append(x)
	#no exit was found so return false
	return False

m = Maze('f1.txt') #initialize maze with selected file.
print(search(m, m.find_start()))