# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 10:24:26 2016

@author: SASedlacek
"""

from actor import Actor
from items import _gear
from kivy.properties import NumericProperty,AliasProperty,ListProperty,ObjectProperty
from collections import OrderedDict
start1 = _gear["Weapon"]["Wooden Sword"]
start2 = _gear["Shield"]["Wooden Shield"]
temp1 = _gear["Weapon"]["Wooden Knife"]


class Player(Actor):
    """This needs a docstring"""
    bagsize = NumericProperty(10)
    bag = ListProperty([temp1])
    xp = NumericProperty(0)
    torches = NumericProperty(0)
    equipped = ObjectProperty(None)
    def __init__(self, **kw):
        super(Player,self).__init__(**kw)
        self.reset()        
        self.name = "Player"
        self.vision = 2
        
    
    def _getstat(self,stat):
        base = self.stats[stat]
        for slot,eq in self.equipped.items():
            if slot == "Acc":
                base += sum([a.stat.get(stat,0) for a in eq])
            elif eq:
                base += eq.stat.get(stat,0)
        return base
    attack = AliasProperty(lambda self:self._getstat("Attack"),None,bind = ["stats","equipped"])
    defense = AliasProperty(lambda self:self._getstat("Defense"),None,bind = ["stats","equipped"])
    accuracy = AliasProperty(lambda self:self._getstat("Accuracy"),None,bind = ["stats","equipped"])
    maxhp = AliasProperty(lambda self:self._getstat("MaxHP"),None,bind = ["stats","equipped"])
    rang = AliasProperty(lambda self:self._getstat("Range"),None,bind = ["stats","equipped"])
    exp = AliasProperty(lambda self:self._getstat("Exp+"),None,bind = ["stats","equipped"])
    goldplus = AliasProperty(lambda self:self._getstat("Gold+"),None,bind = ["stats","equipped"])
        
    def lvlup(self):
        if self.xp - self.xpold < (self.level + 4) ** 2:
            return
        self.level += 1
        self.gold += 50
        #print "Level Up! You now have {} gold".format(self.gold)
        self.stats["MaxHP"] += 10
        self.hp = self.stats["MaxHP"]
        self.xpold = self.xp
        
    def neighbors(self):
        return [(self.x,self.y - 1),(self.x,self.y + 1),
                (self.x + 1,self.y),(self.x - 1,self.y)] 
   
    def reset(self):
        self.bag = []
        self.equipped = OrderedDict((("Weapon",start1),("Shield",start2),("ATop",None),
                                    ("ABottom",None),("Acc",[])))
        self._alive = True
        self.stats = {"Attack":6,"Defense":2,"Accuracy":0.75,"MaxHP":50,"Range":1,"Exp+":1,"Gold+":1}
        self.hp = self.stats["MaxHP"]
        self.xp = 0
        self.xpold = 0
        self.level = 1
        self.gold = 0
        self.facing = 2
        self.torches = 5
        
    def __setstate__(self,state):
        self.hp = state["hp"]
        self.level = state["level"]
        self.name = state["name"]
        self.vision = state["vision"]
        self.stats = state["stats"]
        self.xp = state["xp"]
        self.torches = state["torches"]
        self.gold = state["gold"]
        self.bag = [_gear[c][n] for c,n in state["bag"]]
        for s in self.equipped:
            if state["equipped"][s] is not None:
                if s == "Acc":
                    self.equipped[s] = [_gear[c][n] for c,n in state["equipped"][s]]
                else:
                    c,n = state["equipped"][s]
                    self.equipped[s] = _gear[c][n]
            else:
                self.equipped[s] = None
    def __getstate__(self):
        bag = [(b.category,b.name) for b in self.bag]
        equipped = {}
        for s,e in self.equipped.items():
            if e is not None:
                if s == "Acc":
                    equipped[s] = [(a.category,a.name) for a in e]
                else:   
                    equipped[s] = (e.category,e.name)
            else:
                equipped[s] = None
        return {"hp":self.hp,"level":self.level,"name":self.name,
                "vision":self.vision,"stats":self.stats,"xp":self.xp,
                "torches":self.torches,"bag":bag,"equipped":equipped,"gold":self.gold}
    
    """def getthings(self,item):
        if len(self.bag) == self.bagsize + 1:
            print "Stop hoarding things."
            return
        self.bag.append(item)
        
    def dropthings(self,item):
        if item not in self.bag:
            print "Find one of those then you can drop it (づ'ヮ')づ"
            return
        self.bag.remove(item)
        
         
    def liststats(self):
        print "Xp:",self.xp
        print "Xp to next lvl:",((self.level + 4) ** 2) - self.xp
        print "% to next lvl: {}%".format(int(((self.xp-self.xpold/((self.level + 4) ** 2) - self.xpold))*100))
        print "Level:",self.level
        print "Gold:",self.gold
        print "Health Points:",self.hp
        print "Attack:",self.attack
        print "Defense:",self.defense
        print "Max Health:",self.maxhp
        print "Hit Chance: {}%".format(int(self.accuracy*100))
    
    def equip(self,item):
        #print item.category
        slot = {"Weapon":"Weapon","Shield":"Shield","ATop":"Armor1",
                "ABottom":"Armor2","Accessory":"Acc"}[item.category]
        if item not in self.bag:
            #print "Maybe you should go shopping..."
            return
        if slot not in self.equipped:
            #print "How many extra bodyparts do you have?"
            return
        if item.category == "Accessory":
            if len(self.equipped["Acc"]) == 3:
                #print "You have 3 Accessories equipped:"
                #print "\n".join(self.equipped["Acc"])
                accname = getinput("Which one would you like to remove")
                for a in self.equipped["Acc"]:
                    if accname.lower() in a.name.lower():
                        olditem = a
                        break
                else:
                    #print "Thats not a part of this outfit."
                self.equipped["Acc"].remove(olditem)
                self.bag.append(olditem)
                #print "Dequipped {}".format(olditem.name)
            self.equipped["Acc"].append(item)
            self.bag.remove(item)
            #print "Equipped {}\n".format(item.name)
            return
                            
        self.bag.remove(item)
        if self.equipped[slot]:
            olditem = self.equipped.pop(slot)
            self.bag.append(olditem)
            print "Dequipped {}".format(olditem.name)
            
        self.equipped[slot] = item
        print "Equipped {}\n".format(item.name)"""
        #FIX THIS!!!!!!!!!!!!!