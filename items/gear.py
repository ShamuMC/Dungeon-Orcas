# -*- coding: utf-8 -*-
"""
Created on Thu Nov 05 09:58:20 2015

@author: SASedlacek
"""
from collections import defaultdict
from db import session,Items

itemsdb = session.query(Items).all()


#_gear = {"Weapons":{},"Shields":{},"Accs":{},"Armor":{}}
#numberlist = {0:[],1:[],2:[],3:[],4:[]}



class Item(object):
    def __init__(self,item):
        self.name,self.rarity,self.stat = item
               

accstats = {"acura":"Accuracy","defense":"Defence","attack":"Attack","gold+":"Gold+",
            "exp+":"Exp+","hp":"MaxHP","range":"Range"}

_gear = defaultdict(dict)
numberlist = defaultdict(list)

def rep(self):
    return "{}: {}".format(self.category,self.name)

slots = dict(zip(range(5),[type(cat,(Item,),{"category":cat,"__str__":rep}) for cat in ["Weapon","Shield","ATop","ABottom","Accessory"]]))
stats = dict(zip(["Attack","Defense","Range","Accuracy","Exp+","Gold+","MaxHP"],
                 ["attack","defense","rang","accuracy","exp","gold","maxhp"]))
def assign(item):
    cls = slots[item.slot]
    stat = {x:getattr(item,stats[x]) for x in stats.keys()}
    params = [item.name,item.rarity,stat]
    return cls(params)
    
for i in itemsdb:
    temp = assign(i)
    _gear[temp.category][temp.name] = temp
    numberlist[temp.rarity].append(temp)

    
    