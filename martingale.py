import random
import numpy as np
import matplotlib.pyplot as plt

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

    def __init__(self,stake,bank,games,odds=2,chance=0.5,simulations=1):
        self.stake = stake
        self.bank = bank
        self.games = games
        self.odds = odds
        self.chance = chance
        self.simulations = simulations
        
    def toss(self):
        return random.random()
    
    def simulate(self):
        stake = self.stake
        bank = self.bank
        tosses = {}
        for x in range(1,self.games+1):
            heads = self.toss()
            if heads <= self.chance:
                bank = bank + stake*(self.odds-1)
                stake = self.stake
            else: 
                bank = bank - stake
                stake = stake*2
            if stake > bank:
                stake = bank
            tosses[x] = bank - self.bank
        return tosses
    
    def montecarlo(self):
        results = 0
        results2 = 0
        for x in range(self.simulations):
            s = self.simulate()
            if s[self.games] == -self.bank:
                results += 1
            elif s[self.games] < 0 and s[self.games]!=-self.bank:
                results2 += 1
        return float(results+results2)/float(self.simulations),\
        float(results)/float(self.simulations),float(results2)/float(self.simulations)
    
    def chartpnl(self,result):
        tosses = list(result.keys())
        bank = list(result.values())
        plt.plot(tosses, bank, '-') 
    
m = martingale(1,200,100)
c = m.bustchance()
print(c)

g = game(1,200,100,simulations=10000)
t = g.montecarlo()
print(t)

g.chartpnl(g.simulate())