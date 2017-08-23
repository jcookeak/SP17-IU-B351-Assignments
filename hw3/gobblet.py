from threading import Thread
import threading
from time import sleep
from math import inf
import sys
import copy
import random

def exit(string):
	print(string)
	sys.exit()

#possible wins: 10
# 4 horizontal rows
# 4 vertical columns
# 2 diagonals
#
wins = [
[(0,0), (0,1), (0,2), (0,3)],
[(1,0), (1,1), (1,2), (1,3)],
[(2,0), (2,1), (2,2), (2,3)],
[(3,0), (3,1), (3,2), (3,3)],
[(0,0), (1,0), (2,0), (3,0)],
[(0,1), (1,1), (2,1), (3,1)],
[(0,2), (1,2), (2,2), (3,2)],
[(0,3), (1,3), (2,3), (3,3)],
[(0,0), (1,1), (2,2), (3,3)],
[(0,3), (1,2), (2,1), (3,0)]
]

heuristic_arr = [
[0, -10, -100, -1000, -10000],
[10, 0, 0, 0, 0],
[100, 0, 0, 0, 0],
[1000, 0, 0, 0, 0],
[10000, 0, 0, 0, 0]
]

# heuristic_arr = [
# [0, -10, -100, -1000, -10000],
# [10, 0, -10, -100, 0],
# [100, 10, 0, 0, 0],
# [1000, 100, 0, 0, 0],
# [10000, 0, 0, 0, 0]
#]
def heur(game):
	t = 0
	for i in range(len(wins)):
		p1, p2 = 0, 0
		for j in range(len(game.board)):
			temp = wins[i][j]
			piece = game.board[temp[0]][temp[1]][0]
			if piece[0] == 'w':
				p1 += 1
			if piece[0] == 'b':
				p2 += 1
			t += heuristic_arr[p1][p2]
	return t

#pass in copy of game
def alphabeta(game, depth, alpha, beta, max_player):
	if depth == 0 or len(game.get_moves(game.active_player)) == 0:
		return heur(game)
	if max_player:
		v = -inf
		legal_moves = game.get_moves(game.active_player)
		random.shuffle(legal_moves)
		for x in legal_moves:
			game.make_move(x, game.active_player)
			v = max(v, alphabeta(game, depth - 1, alpha, beta, False))
			game.undo_move(x)
			alpha = max(alpha, v)
			if beta <= alpha:
				#return beta
				break #cut off beta branch
		return v
	else:
		v = inf
		legal_moves = game.get_moves(game.active_player)
		random.shuffle(legal_moves)
		for x in legal_moves:
			game.make_move(x, game.active_player)
			v = min(v, alphabeta(game, depth - 1, alpha, beta, True))
			game.undo_move(x)
			beta = min(beta, v)
			if beta <= alpha:
				#return alpha
				break # cut off alpha branch
		return v


class player(object):
	def __init__(self, color):
		self.color = color # 3 stacks of 4
		self.stack_num = 3
		self.stack = [4 for _ in range(self.stack_num)]

	def __str__(self):
		return self.color

	def make_move(self,game, moves):
		board = game.board
		print('legal move') 
		print(moves)
		print ("play from stack (s) or move piece (m)?")
		while True:
			try:
				self.arr = input()
				if self.arr == 's':
					print("input stack, x, y (comma seperated, no spaces)")
					while True:	
						try:
							self.arr = input()
							self.move = list(map(int,self.arr.split(',')))
							self.move = ['s'] + self.move
							print(self.move)
							#correct len of input
							if len(self.move) != 4:
								raise ValueError
							if tuple(self.move) not in moves:
								raise ValueError
							break;
						except ValueError:
							print('illegal input! please retry')
				if self.arr == 'm':
					while True:
						try:
							print("input x1,y1,x2,y2 where (x1,y1) is from and (x2,y2) is to")
							self.arr = input()
							self.move = list(map(int,self.arr.split(',')))
							self.move = ['m'] + self.move
							# check input size
							if len(self.move) != 5:
								raise ValueError
							if tuple(self.move) not in moves:
								raise ValueError
							break;
						except ValueError:
							print('input legal move')
				break;
			except ValueError:
				print('input m or s')

		# stack num, x, y
		print(tuple(self.move))
		return self.move

class robot(player):
	def __init__(self, color, diff):
		super(robot, self).__init__(color)
		self.diff = diff

	def make_move(self, game, moves):
		#inverse of minmax b/c make move changes active player
		if self.color == 'w':
			self.player_minmax = False
		else:
			self.player_minmax = True 
		self.search_list = []
		g = copy.deepcopy(game)
		random.shuffle(moves)
		for x in moves:
			g.make_move(x, g.active_player)
			self.search = alphabeta(g, self.diff+1, -inf, inf, self.player_minmax)
			self.search_list.append([self.search, x])
			g.undo_move(x)

		if self.color == 'w':
			# print('moves',self.search_list)
			# print('max move',max(self.search_list))
			return max(self.search_list)[1]
		else:
			# print('moves',self.search_list)
			# print('min move', min(self.search_list))
			return min(self.search_list)[1]


class gobblet(object):

	def __init__(self, players, tlimit): 
		self.tlimit = tlimit * 60
		self.outoftime = False
		self.n = 4
		self.board = [[["  "] for _ in range(self.n)] for _ in range(self.n)];
		self.player1 = players[0] #robot('w', 2) #player('w')
		self.player2 = players[1]#robot('b', 2) #player('b')
		self.active_player = self.player1
		self.play_history = []
		self.stack_history = []

	def __str__(self):
		self.string = "active player: " + str(self.active_player) + '\n'
		self.string = self.string + '- 0  1  2  3 -' + '\n'
		for y in range(len(self.board)):
			self.string = self.string + str(y) + '|'
			for x in range(len(self.board[y])):
				self.string = self.string + str(self.board[x][y][0]) + '|'
			self.string = self.string + "\n"
		self.string = self.string + 'player w stack:' + str(self.player1.stack) + '\n'
		self.string = self.string + 'player b stack:' + str(self.player2.stack) + '\n' 
		return self.string

	# get legal moves for a player
	def get_moves(self, player):
		self.moves = []
		if self.check_win() or self.check_draw():
			return self.moves
		# pieces from stack go on empty spaces
		# if three in a row of opponents pieces, can gobble their piece
		for s in range(len(player.stack)):
			for x in range(len(self.board)):
				for y in range(len(self.board[x])):
					if player.stack[s] > 0 and self.check_gobble(player.stack[s], x, y) and self.check_3(x,y):
						self.moves.append(('s',s,x,y))
		#pieces on the board can move to an empty space or gobble a legal space
		for x1 in range(len(self.board)):
			for y1 in range(len(self.board)):
				if self.board[x1][y1][0][0] == player.color:
					for x2 in range(len(self.board)):
						for y2 in range(len(self.board)):
							if self.check_gobble(int(self.board[x1][y1][0][1]),x2,y2):
								self.moves.append(('m', x1,y1,x2,y2))
		return self.moves

	def active_game(self):
		if not self.check_draw():
			if not self.check_win():
				if len(self.get_moves(self.active_player)) > 0:
					return True
		return False

	def check_gobble(self, a, x, y):
		# '  ' for unused space to make pretty print
		if a < 0:
			return False
		#prevents negative pieces on board
		elif self.board[x][y][0][1] == '-':
			return False
		if a >= 0 and self.board[x][y][0] == '  ':
			return True
		# b[0] is color b[1] represents size from 1-4
		elif a >= 0 and a > int(self.board[x][y][0][1]):
			return True
		else:
			False
	#check to see if a piece may be gobbled
	def check_3(self,x,y):
		if self.board[x][y][0][0] == ' ':
			return True
		if self.active_player == self.player1 : self.opp_color = self.player2.color
		else: self.opp_color = self.player1.color
		#check right side
		if x < 2 and y <= 3:
			if self.board[x][y][0][0] == self.board[x+1][y][0][0] == self.board[x+2][y][0][0] == self.opp_color:
				return True
		# check left side
		if x >= 2:
			if self.board[x][y][0][0] == self.board[x-1][y][0][0] == self.board[x-2][y][0][0] == self.opp_color:
				return True
		#check above
		if y < 2:
			if self.board[x][y][0][0] == self.board[x][y+1][0][0] == self.board[x][y+2][0][0] == self.opp_color:
				return True
		if y >= 2:
			if self.board[x][y][0][0] == self.board[x][y-1][0][0] == self.board[x][y-2][0][0] == self.opp_color:
				return True
		#diagonals
		if x < 2 and y >= 2:
			if self.board[x][y][0][0] == self.board[x+1][y-1][0][0] == self.board[x+1][y-2][0][0] == self.opp_color:
				return True
		if x >=2 and y >= 2:
			if self.board[x][y][0][0] == self.board[x-1][y-1][0][0] == self.board[x-1][y-2][0][0] == self.opp_color:
				return True
		if x >= 2 and y < 2:
			if self.board[x][y][0][0] == self.board[x-1][y+1][0][0] == self.board[x-2][y+2][0][0] == self.opp_color:
				return True
		if x < 2 and y < 2:
			if self.board[x][y][0][0] == self.board[x+1][y+1][0][0] == self.board[x+2][y+2][0][0] == self.opp_color:
				return True
		# check interior diagonals
		if (x >=1 and x < 3) and (y >=1 and y < 3):
			if self.board[x][y][0][0] == self.board[x+1][y-1][0][0] == self.board[x-1][y+1][0][0] == self.opp_color:
				return True
			if self.board[x][y][0][0] == self.board[x-1][y-1][0][0] == self.board[x+1][y+1][0][0] == self.opp_color:
				return True
		return False

		#piece in center (check l+r and t+b)

	def check_draw(self):
		if len(self.play_history) >= 6:
			if (self.play_history[-1] == self.play_history[-3] == self.play_history[-5]):
				if(self.play_history[-2] == self.play_history[-4] == self.play_history[-6]):
					return True
		return False

	def check_win(self):
		# [x][y][slot][char]
		b = self.board
		for x in range(self.n):
			if b[x][0][0][0] == b[x][1][0][0] == b[x][2][0][0] == b[x][3][0][0] and b[x][0][0] != '  ':
				#print('game finished')
				return True
		for y in range(self.n):
			if b[0][y][0][0] == b[1][y][0][0] == b[2][y][0][0] == b[3][y][0][0] and b[0][y][0] != '  ':
				#print('game finished')
				return True
		#diagonal 0,0 -> 3,3
		for x in range(self.n):
			if b[0][0][0][0] == b[1][1][0][0] == b[2][2][0][0] == b[3][3][0][0] and b[0][0][0] != '  ':
				#print('game finished')
				return True
		#diagonal 0,3 -> 3,0
		for y in range(self.n):
			if b[0][3][0][0] == b[1][2][0][0] == b[2][1][0][0] == b[3][0][0][0] and b[3][0][0] != '  ':
				#print('game finished')
				return True
		return False


	def start_turn(self):
		while self.active_game():
			print(self)
			t = threading.Timer(self.tlimit,exit,args=("out of time.  You lose!",))
			t.start()
			try:
				move = self.get_move() #block the main thread
				self.make_move(move, self.active_player)
				if self.check_draw():
					print("The game is a draw")
					t.cancel()
					t.join()
					sys.exit()
				if self.check_win():
					print('the game is over')
					if(self.active_player.color == 'b'):
						print("Player 1 wins")
					else:
						print("Player 2 wins")
					print(self)
					t.cancel()
					t.join()
					sys.exit()
			except KeyboardInterrupt:
				t.cancel()
				t.join()
				sys.exit()
			# if get_move succeds then cancel is called and thread is joined
			t.cancel()
			t.join()
			
		sys.exit()
		

	def get_move(self):
		return self.active_player.make_move(self, self.get_moves(self.active_player))
	def make_move(self,move, player):
		self.play_history.append([move, player.color])
		self.stack_history.append([player.stack, player.color])
		if move[0] == 's':
			self.board[move[2]][move[3]] = [player.color + str(player.stack[move[1]])] + self.board[move[2]][move[3]]
			player.stack[move[1]] = player.stack[move[1]] - 1
		if move[0] == 'm':
			#to
			self.board[move[3]][move[4]] = [self.board[move[1]][move[2]][0]] + self.board[move[3]][move[4]]
			self.board[move[1]][move[2]].pop(0)
		if self.active_player is self.player1: self.active_player = self.player2
		else: self.active_player = self.player1

	#undo move
	def undo_move(self, move):
		#print(self)
		#print('player stack undoing', move)
		#find player color based on move history
		t_hist = [item[0] for item in self.play_history]
		self.hindex = len(t_hist) -1 - t_hist[::-1].index(move)
		#print('spots away from end', len(t_hist) - 1 - self.hindex)
		if 'w' == self.play_history[self.hindex][1]:
			self.p = self.player1
		else: 
			self.p = self.player2
		del self.play_history[-1]
		if move[0] == 's':
			self.board[move[2]][move[3]].pop(0)
			#print('stack', self.p.stack)
			self.p.stack[move[1]] = self.p.stack[move[1]] + 1
		if move[0] == 'm':
			#reverse make_move()
			self.temp = self.board[move[3]][move[4]].pop(0)
			self.board[move[1]][move[2]] = [self.temp] + self.board[move[1]][move[2]]
		#change active player
		del self.stack_history[-1]
		self.active_player = self.p

def gobby(players, level, time):
	if (players == 'h2'):
		players = (player('w'), player('b'))
	elif(players == 'hr'):
		players = (player('w'), robot('b', level))
	elif(players == 'rh'):
		players = (robot('w', level), player('b'))
	elif(players == 'r2'):
		players = (robot('w', level), robot('b', level))
		
	else:
		print("illegal player selection")
		sys.exit()
	g = gobblet(players, time)
	g.start_turn()


#################
gobby('r2',2,2.5)