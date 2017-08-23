import random as rn

#values of rock, paper, scissors
r,p,s = 0,1,2
#dictionary e.g., rock beats scissors
ws = {r:s, p:r, s:p}

nogames = int(input("Number of games? "))

totgames = 0
compwins = 0
rbwins = 0
ties = 0

gamehistory = []

def select_move(history):
    rand = rn.randrange(0,2,1)
    rbmove = 0
    #flip a coin, if 0 go for random approach, if 1 go for pattern
    if (rand == 0):
        #start at 0 go to 3 exclusive, stepping by 1
        rbmove = rn.randrange(0,3,1)
    #pattern: start with s, bias for p
    else:
        if(history == []):
            rbmove = 2
        #if opponent throws r last game, w throw p
        elif (history[-1][1] == 0):
            rbmove = 1
        #if opponent throws p last game, we throw p
        elif (history[-1][1] == 1):
            rbmove = 1
        #s we throw r
        else:
            rbmove = 0
    return rbmove

while totgames < nogames:
     # human = int(input("r=0,p=1,s=2 "))
     robby = select_move(gamehistory)  #int(rn.uniform(0,3))
     comp = rn.randrange(0,3,1)
     gamehistory.append([robby, comp])

     print("Robby: {0}, Comp: {1}".format(robby, comp))

     if ws[comp] == robby:
        compwins += 1
     elif ws[robby] == comp:
        rbwins += 1
     else:
        ties += 1
     totgames += 1

v = list(map(lambda x: 100*x/totgames, [compwins, rbwins, ties]))
print("Stats\ncw% = {0}, rb% = {1}, ties% = {2}".format(*v))

