"""A Module to end all die rolling"""
import random

class ArbitraryDie(object):
    """A Class that generates an arbitrary int"""
    def __init__(self,minside,maxside):
        self.low,self.high = minside,maxside
        
    def roll(self,n = 1):
        result = [random.randint(self.low, self.high) for i in range(n)]
        if n == 1:
            return result[0]
        return result

class Dice(ArbitraryDie):
    """A Class that rolls a die """
    def __init__(self, num_sides):
        super(Dice,self).__init__(1,num_sides)


  