from Maze import *
from math import *

#simple pythagorian's throrem with floor to ignore decimal points
#used as heuristic estimate from a current node and the goal
def dist_between(point1, point2):
	return floor(sqrt((point1[0] + point2[0])^2 + (point1[1] + point2[1])^2))

def a_star(graph, start, end):
	visited, stack = [], [start]
	parent = {} #dict used to reconstruct path
	g_score = {} 
	g_score[start] = 0
	f_score = {}
	f_score[start] = dist_between(start,end)
	while stack:
		current = stack.pop()
		if current == end:
			return path_traveled(parent, current) 
		visited.append(current)
		for x in graph.get_sibling(current[0],current[1]):
			if x in visited:
				continue
			# current g_score^ and distance between current and its neighbors
			g_score_h = g_score[current] + dist_between(current, x) 
			if x not in visited:
				stack.append(x)
			elif g_score[x] < g_score_h:
				continue
			parent[x] = current
			g_score[x] = g_score_h
			f_score[x] = g_score[x] + dist_between(x,end)
	return False

#digs through provided dict and reconstructs the path taken
def path_traveled(prev, current):
	path = [current]
	while current in prev:
		current = prev[current]
		path.append(current)
	path.reverse()
	return path


m = Maze('f.txt') #initialize maze with selected file.
#perform a* seach on each exit node, return shortest of these.

mins = []

e = m.find_exits(m.find_start())[0]
print("distance between start and finish: ", 
	dist_between(m.find_start(), e))

#more than one exit may exist, therefore find the closest one.
for x in m.find_exits(m.find_start()):
	p = a_star(m, m.find_start(), x)
	#only add if a path exists
	if p:
		mins.append((len(p), p)) #store paths and their lengths

#make sure a path exists before trying to get second element in tuple
if len(mins) > 0:
	print(min(mins)[1])
else:
	print('no path exists')
