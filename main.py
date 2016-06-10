# -*- coding: utf-8 -*-s
"""
Created on Tue Apr 19 09:40:59 2016

@author: SASedlacek
"""

from kivy.app import App
from interface import LayeredMap,GameOver,Console
from kivy.clock import Clock
from kivy.properties import ObjectProperty,NumericProperty,DictProperty
from kivy.core.window import Window
#from kivy.uix.screenmanager import Screen,ScreenManager
from mazegen import Maze
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from cfg import KEYBINDS as keys#,SAVEPATH as savepath
#from savegame import save,load
#from os.path import isfile, join
from engine import Engine
#import os
from utils import facing
mapsize = 21
initlevel = 1
commands = {keys["Up"]:"n",keys["Left"]:"w",keys["Down"]:"s",keys["Right"]:"e",
                keys["Attack"]:"",keys["Quit"]:"",keys["Stats"]:"",keys["Reset"]:"",
                keys["Equip"]:"",keys["Interact"]:"",keys["Load"]:"",keys["Debug"]:"","8":""}
gameoversound = SoundLoader.load("sounds/death.wav")

class GameAPP(App):
    _maze = ObjectProperty(None)
    _map = ObjectProperty(None,force_dispatch = True)
    engine = ObjectProperty(None)
    _lighting = DictProperty({})
    interface = ObjectProperty(None)
    console = ObjectProperty(None)
    def output(self,text):
        self.console.add(text)        
    def parse(self,keyboard,keycode,text,modifiers):
        if text not in "wasdf":
            return
        self.engine.parse(text)
        self.interface.update()
        #print keyboard,keycode,text,modifiers
    def build(self):
        self._maze = Maze()
        self.title = "can't think of one now"
        self.icon = "graphics/icon.png"
        #self.root = ScreenManager()
        self.root = BoxLayout(orientation = "horizontal")
        self.keyboard = Window.request_keyboard(None,self.root)
        self.keyboard.bind(on_key_down = self.parse)
        self.reset()
        #Clock.schedule_interval(self.update,0.5)
        return self.root
    def update(self,dt):
        self.engine.monaction()
        self.engine.cleanup()
        if not self.engine.player._alive:
            gameoversound.play()
            Clock.unschedule(self.update)
            popup = GameOver()
            popup.bind(on_dismiss = lambda x:self.reset())
            popup.open()
        self.interface.update()
    def reset(self):
        self.root.clear_widgets()
        #screen = Screen(name = "Game")
        shapep = int(mapsize)+((initlevel-1)*5)
        if shapep % 2 == 0:
            shapep += 1
        self._map = self._maze((shapep,shapep),0.75,0.75,new = True)
        self.engine = Engine(_maze = self._map,_level = initlevel,outputfunc = self.output)
        self.interface = LayeredMap(_shape = shapep,_map = self.engine._map)
        self.root.add_widget(self.interface)
        self.console = Console()
        self.root.add_widget(self.console)
        #screen.add_widget(self.interface) 
        #self.root.add_widget(screen)
        #self.root.current = "Game"
        Clock.schedule_interval(self.update,0.5)
if __name__ == "__main__":
    GameAPP().run()