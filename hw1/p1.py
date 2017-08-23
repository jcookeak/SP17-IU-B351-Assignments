adj = {'U' : ['L', 'C'], 
'L' : ['U','D'], 
'C' : ['U','I'], 
'I' : ['C'],
'D' : ['L','F','K'],
'F' : ['D','E'],
'K' : ['D', 'G'],
'E' : ['F'],
'G' : ['K','J','H'],
'J' : ['G','B'],
'H' : ['G','B'],
'B' : ['J','H','A'],
'A' : ['B']
} 

adj_set = {'U' : set(['L', 'C']), 
'L' : set(['U','D']), 
'C' : set(['U','I']), 
'I' : set(['C']),
'D' : set(['L','F','K']),
'F' : set(['D','E']),
'K' : set(['D', 'G']),
'E' : set(['F']),
'G' : set(['K','J','H']),
'J' : set(['G','B']),
'H' : set(['G','B']),
'B' : set(['J','H','A']),
'A' : set(['B'])
} 

def dfs(graph, initial):
	visited, stack = [], [initial]
	while stack:
		vertex = stack.pop()
		if vertex not in visited:
			visited.append(vertex)
			for x in graph[vertex]:
				stack.append(x)
	return visited

print(dfs(adj, 'U'))