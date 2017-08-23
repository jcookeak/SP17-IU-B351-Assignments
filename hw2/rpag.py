import random as rn

#values of rock, paper, scissors
r,p,s = 0,1,2
#dictionary e.g., rock beats scissors
ws = {r:s, p:r, s:p}

h_balance = 100
c_balance = 100

nogames = int(input("Number of games? "))

totgames = 0
compwins = 0
humwins = 0
ties = 0

gamehistory = []

#can't play without money
while totgames < nogames and h_balance > 0 and c_balance > 0:
     print("your balance is currently", h_balance)
     #tell user what the max bet is
     print("max bet is :", min(h_balance, c_balance)) 
     h_bet = int(input("make a bet "))
     #check bets for legality
     while (h_bet > h_balance or h_bet < 1 or h_bet > min(h_balance, c_balance)) :
        print('illegal bet')
        h_bet = int(input("make a 'legal' bet "))
     human = int(input("r=0,p=1,s=2 "))
     comp = rn.randrange(0,3,1)
     #don't let comp's bet exceed min balance between players
     comp_bet = rn.randrange(0,min(c_balance,h_balance),1)
     max_bet = max(h_bet, comp_bet)
     gamehistory.append([human, comp])

     print("Human: {0}, Comp: {1}".format(human, comp))

     if ws[comp] == human:
        compwins += 1
        c_balance += max_bet
        h_balance -= max_bet
     elif ws[human] == comp:
        humwins += 1
        h_balance += max_bet
        c_balance -= max_bet
     else: #no money changes hands for tie
        ties += 1
     totgames += 1

     print("your balance is now", h_balance)
     print("comp's balance is now", c_balance)

v = list(map(lambda x: 100*x/totgames, [compwins, humwins, ties]))
print("Stats\ncw% = {0}, hm% = {1}, ties% = {2}".format(*v))

