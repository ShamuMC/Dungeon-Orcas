# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 21:33:19 2015

@author: benny

Direction priority: lrdu
"""
#import pdb
from numpy.random import ranf
from utils import facing,Dice
from actors import Player,Monster
from items import Chest
from gmap import Map
from kivy.event import EventDispatcher
from kivy.properties import (NumericProperty,ListProperty,
                             BooleanProperty,ObjectProperty)


dLife = Dice(4)


#class Dungeon(self,difficulty):
 #   def __init__(self):
  #      pass


"""def run(self):
        while self.player._alive:  
            action = getinput("")
            action = action.lower()
            if action:
                action = action[0]
            if action in self.commands:
                self.parse(action)
                self.monaction()
                self.cleanup()
                self._map.redraw()
            print self._map
            
    def parse(self,action):
        """"""
        if action == keys["Quit"]:
            sys.exit()
        if action in [keys["Up"],keys["Left"],keys["Down"],keys["Right"]]:
            self.move(self.commands[action])
        elif action == keys["Reset"]: 
            self._level = 1
            self.reset(True)
            
        elif action == keys["Stats"]:
            self.player.liststats()
            print "----<Inv>----"
            self.player.listinv()
            print "----<Game>----"
            print "Level#: {}".format(self._level)
            print "Monsters Remaining:",len(self.monsters)
            print "Unclaimed Chests:",len([chest for chest in self._map.chests if chest.inv != [None]])
            debug("Debug mode: {}".format({True:"Enabled",False:"Disabled (you shouldnt see this)"}[self.debug]),self.debug)
            
            
            
        elif action == keys["Attack"]:
            for x,y in self.player.loe:
                target = self._map[x,y]
                if target in self.monsters:
                    self.attack(self.player,target)
                    break 
                if isinstance(target,Wall):
                    print "You attack the walls"
                    break
            else:
                print "What are you doing?"
                
        elif action == keys["Equip"]:
            self.player.listinv()
            action2 = raw_input("Equip: ")
            for i in self.player.bag:
                if action2 in i.name:
                    self.player.equip(i)
                    break
                
                    
        elif action == keys["Interact"]:
            #Interact Key
            x,y = self.player.loe[0]
            if isinstance(self._map[x,y],Chest):
                if not self._map[x,y].inv:
                    print "Nothing Here"
                    return
                else:
                    chest = self._map[x,y].inv
                    for i in chest:
                        
                        j = chest.index(i) + 1
                        print "Slot {}: {}".format(j,[i.name,"Empty"][i == None])
                        print self._map
                    action2 = raw_input("What Item To Take \n: ")
                    for i in chest:
                        g = i.name.split(" ")
                        f = action2.split(" ")
                        for c in f:
                            for v in g:
                                if str(c.lower()) == str(v.lower()):
                                    self.player.getthings(i)
                                    chest.remove(i)
            elif self._map[x,y] == self._map.exit and self.player.facestr == "n":
                self.nxtlevel()
                
            else:
                if isinstance(self._map[x,y],Wall):
                    if self.player.torches > 0:    
                        self._map.placels(x,y)
                        self.player.torches -= 1
                    else:
                        print "No more torches for you."
                                                
        elif action == keys["Load"]:
            onlyfiles = [f for f in os.listdir(savepath) if isfile(join(savepath, f))]
            files = []
            for i in onlyfiles:
                print i[:-4]
                files.append(i[:-4])
            loadfile = getinput("")
            if loadfile in files:    
                loadfile = "{}.sav".format(loadfile)
                self.__setstate__(load(loadfile))
            
        elif action == keys["Debug"]:
            if self.debug:
                self.debug = False
            else:
                self.debug = True
        elif action == "8":
            save(self)"""


def genmonster(level):
        if ranf() <= 0.25:
            rang = 3 
            kind = "ranged"
        else:
            rang = 1
            kind = "melee"
        return Monster(level = level,r = rang,kind = kind)



class Engine(EventDispatcher):
    """This needs a docstring"""
    _level = NumericProperty(1)
    _map = ObjectProperty(None)
    monsters = ListProperty([])
    player = ObjectProperty(None,allownone = True)
    debug = BooleanProperty(False)
    outputfunc = ObjectProperty(None)
    _maze = ObjectProperty(None,force_dispatch = True)
    def __init__(self, **kw):
        super(Engine,self).__init__(**kw)        
        self.player = Player()
        self.monsters = [genmonster(self._level) for i in range(self._level)]
        self._map = Map(player = self.player,monsters = self.monsters,
                        _level = self._level,_Z = self._maze)

    def __setstate__(self,state):
        self._map.__setstate__(state["map"])
        self.player.__setstate__(state["player"])
        self._level = state["level"]
        for monster,mstate in zip(self.monsters,state["monsters"]):
            monster.__setstate__(mstate)
    
    def __getstate__(self):
        return {"map":self._map.__getstate__(),"player":self.player.__getstate__(),
        "monsters":[m.__getstate__() for m in self.monsters],"level":self._level}
    
    def parse(self,text):
        if text in "adsw":
            self.move("adsw".index(text))
        if text in "f":
            for x,y in self.player.loe:
                if self._map[x,y]:
                        break
                for m in self.monsters:
                    if m.coords == [x,y]:
                        self.attack(self.player,m)
                        break
    def nxtlevel(self):
        self._level += 1
        self.reset(False)
        self.player.xp += 10
        self.player.torches += 2
                                            
    def cleanup(self):
        """"""
        for monster in self.monsters:
            if monster.hp <= 0:
                self.player.xp += (monster.level * 5) * self.player.exp
                self.player.gold += (monster.level * 10) * self.player.goldplus
                if dLife.roll() == 1:
                    life = 20
                    maxhp = getattr(self.player,"maxhp")
                    while True:
                        if self.player.hp + life > maxhp:
                            life -= 1
                        else:
                            break
                    if life > 0:
                        pass
                        self.outputfunc("+{} hp".format(life))
                    self.player.hp += life
                        
        self.monsters = filter(lambda m: m.hp > 0,self.monsters)
        self._map.monsters = self.monsters
        if self.player.coords == self._map.exit:
            self.nxtlevel()
            return
            
        if self.player.hp <= 0:
            self.player._alive = False
            #player dead
            #replay = raw_input("Retry? y/n: ")
            #if replay == "y":
            #    self.reset(True)
                
            #    self._map.reset(1)
            #else:
            #   sys.exit()
        else: 
            self.player.lvlup()
            
    def reset(self,player):
        if player:
            self.player.reset()
        self.monsters = [genmonster(self._level) for i in range(self._level)]
        self._map.monsters = self.monsters
        self._map.reset(self._level)  

    def attack(self,atk,defend):
        """"""
        if ranf() <= atk.accuracy:
            hit = atk.attack - defend.defense
            if type(atk) == Player and self.player.equipped["Weapon"].stat.get("backstab",0) == 1:
                hit = atk.attack*3
            if ranf < 0.05:
                hit = hit*2
            if hit < 0:
                hit = 0
            defend.hp -= hit
            self.outputfunc(" A Hit! {} has {} hp remaining".format(defend.name,defend.hp))
        else:
            self.outputfunc("{} missed!".format(atk.name))
           
    def move(self, direction):
        dx,dy = facing(self.player,direction)
        if not self._map.passable(self.player.mapx + dx,self.player.mapy + dy):
            return
            
        if (self.player.mapx + dx,self.player.mapy + dy) == self._map.entrance:
            self.outputfunc("You bang on the door")
            
            return
        
        if (self.player.mapx + dx,self.player.mapy + dy) == self._map.exit and direction != 3:
            return
            
        self.player.move(dx, dy)
    def monaction(self):
        for monster in self.monsters:
            monster.ai(self._map,self)