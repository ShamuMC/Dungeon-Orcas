# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 09:45:31 2015

@author: SASedlacek
"""
import numpy as npy
from numpy.random import RandomState as randstate
from utils import Dice
    
class Maze(object):       
    def __init__(self,seed = None):
        self.rand = randstate()
        if seed is None:
            self.seed = self.rand.random_integers(1e9)
        else:
            self.seed = seed
        
    def __call__(self,shape,density,complexity,boss = False,new = False):
        if not new:    
            self.rand.seed(self.seed)
        complexity = int(complexity * (5 * (shape[0] + shape[1])))
        density    = int(density * (shape[0] // 2 * shape[1] // 2))
            
        Z = npy.full(shape, False, dtype=bool)
        # Fill borders
        Z[0, :] = Z[-1, :] = True
        Z[:, 0] = Z[:, -1] = True
        # Make aisles
        if not boss:
            for i in range(density):
                x, y = (self.rand.random_integers(0, shape[1] // 2) * 2,
                        self.rand.random_integers(0, shape[0] // 2) * 2)
                Z[y, x] = True
                for j in range(complexity):
                    neighbours = []
                    if x > 1:             neighbours.append((y, x - 2))
                    if x < shape[1] - 2:  neighbours.append((y, x + 2))
                    if y > 1:             neighbours.append((y - 2, x))
                    if y < shape[0] - 2:  neighbours.append((y + 2, x))
                    if len(neighbours):
                        y_,x_ = neighbours[self.rand.random_integers(0, len(neighbours) - 1)]
                        if not Z[y_, x_]:
                            Z[y_, x_] = True
                            Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = True
                            x, y = x_, y_
        return Z