# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 09:21:31 2015

@author: SASedlacek
"""
import datetime
import os
import jsonpickle
from cfg import SAVEPATH as savepath
from json import dump,load as jload
from os.path import isfile, join
import pdb


def save(gamestate):
    current = datetime.datetime.today()
    savename = "{}-{}-{} {}_{}.sav".format(current.month,current.day,str(current.year)[2:],current.hour,current.minute)
    
    with open(os.path.join(savepath,savename),'w') as save:
        dump(gamestate.__getstate__(),save)
    print "Game saved as {}".format(savename)
        
def load(filename):
    with open(os.path.join(savepath,filename)) as save:
        return jload(save)