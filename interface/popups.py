# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:00:51 2016

@author: SASedlacek
"""

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
'''#from kivy.lang import Builder


popups = """
<GameOver>:
    title: "You Died"
    BoxLayout:
        orientation: "vertical"
        Label: 
            halign: "center"
            valign: "middle"
            text: "lol\nyou died"
        Button:
            size_hint_y: None
            height: "32dp"
            text: "Reset"
            #on_press: root.dismiss()
"""
#Builder.load_string(popups)'''

class GameOver(Popup):
    def __init__(self,**kw):
        content = BoxLayout(orientation = "vertical")
        content.add_widget(Label(halign = "center",valign = "middle", text = "lol\nyou died"))
        button = Button(size_hint_y = None,height = "32dp", text = "reset")
        content.add_widget(button)
        super(GameOver,self).__init__(title = "You Died",content = content)
        button.bind(on_press = lambda *x:self.dismiss())
    