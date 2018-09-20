import random
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy, scipy.stats

class martingale:
    
    def __init__(self,stake,bank,games,chance=0.5):
        self.stake = stake
        self.bank = bank
        self.games = games
        self.chance = chance
        
    # Calculate how many consecutive losses before balance is gone
    def gamesbust(self):
        cur_bank = self.bank
        cur_stake = self.stake
        count = 0
        while cur_bank > 0:
            cur_bank = cur_bank-cur_stake
            count += 1
            cur_stake = cur_stake * 2
        return count
    
    # Calculate the probability of getting x consecutive losses, x denoted by 'want'
    def heads_in_a_row(self,want):
        a = np.zeros((want + 1, want + 1))
        for i in range(want):
            a[i, 0] = 1 - self.chance
            a[i, i + 1] = self.chance
        a[want, want] = 1.0
        return np.linalg.matrix_power(a, self.games)[0, want]
    
    # Calculates the probablity of losing your balance
    def bustchance(self):
       bust = self.gamesbust()
       prob = self.heads_in_a_row(bust)
       return prob
            
class game:

    def __init__(self,stake,bank,games,odds=2,chance=0.5,simulations=1,coeffs=None):
        self.stake = stake
        self.bank = bank
        self.games = games
        self.odds = odds
        self.chance = chance
        self.simulations = simulations
        self.coeffs = coeffs
        
    def toss(self):
        return random.random()
    
    def simulate(self,games=None,count=False):
        stake = self.stake
        bank = self.bank
        tosses = {}
        headcount = 0
        if games == None:
            games = self.games
        if count == False:
            for x in range(1,games+1):
                if bank != 0:
                    heads = self.toss()
                    if heads < self.chance:
                        bank = bank + stake*(self.odds-1)
                        stake = self.stake
                    else: 
                        bank = bank - stake
                        stake = stake*2
                    if stake > bank:
                        stake = bank
                    tosses[x] = bank - self.bank
            return tosses
        else: 
            for x in range(1,games+1):
                heads = self.toss()
                if heads < self.chance:
                    headcount += 1
            return headcount
    
    def montecarlo(self,games=None,count=False):
        results = 0
        results2 = 0
        profit = 0
        if count == False:
            for x in range(self.simulations):
                if games == None:
                    s = self.simulate()
                else: s = self.simulate(games)
                if s[len(s)] == -self.bank:
                    results += 1
                elif s[len(s)] < 0 and s[len(s)]!=-self.bank:
                    results2 += 1
                profit += s[len(s)]
            return float(results+results2)/float(self.simulations),\
            float(results)/float(self.simulations),float(results2)/float(self.simulations),\
            float(profit)/float(self.simulations)
        else:
            heads = []
            for x in range(self.simulations):
                heads.append(self.simulate(count=True))
            return heads
                
    def chartpnl(self,result):
        tosses = list(result.keys())
        bank = list(result.values())
        plt.plot(tosses, bank, '-') 
        
    def getmean(self):
        return self.simulations * self.chance
    
    def getstd(self):
        return math.sqrt(self.simulations * self.chance * (1 - self.chance))
    
    def plotdist(self):
        result = self.counter(self.montecarlo(count=True))
        k = np.arange(0.75*self.chance*self.games,1.25*self.chance*self.games)
        norm = scipy.stats.binom.pmf(k,self.games,self.chance)*self.simulations
        result = sorted(result.items())
        x,y = zip(*result)
        plt.plot(k,norm,'-')
        plt.plot(x,y,'o')
        plt.show()
    
    def plotexpected(self):
        chance = {}
        for x in self.coeffs:
            self.simulations = x
            a,b,c,p = self.montecarlo(games=x)
            chance[x] = b
        return chance
    
    def counter(self,list1):
        my_dict = {}
        for x in list(set(list1)):
            my_dict[x] = len([elem for elem in list1 if elem == x])
        my_dict = my_dict
        return my_dict

coeffs = list(range(10,2010,10))

for x in coeffs:
    m = martingale(1,500,x)
    c = m.bustchance()
    print(c)

g = game(1,500,1000,simulations=1000,coeffs=coeffs)
g.plotdist()
t = g.montecarlo()
print(t)
d = g.plotexpected()
g.chartpnl(g.plotexpected())