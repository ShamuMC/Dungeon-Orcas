# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 09:56:15 2016

@author: SASedlacek
"""

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import AliasProperty,StringProperty,ListProperty
Builder.load_string("""
<Console>: 
    orientation: "vertical"
    Label:
        text_size: self.size
        valign: "bottom"
        halign: "left"
        text: root.text
""")
class Console(BoxLayout):
    msg = ListProperty([])
    def add(self,inpu):
        if len(self.msg) >= 20:
            self.msg = self.msg[1:]
        self.msg.append(inpu)
    def _get_text(self):
        return "\n".join(self.msg)
    text = AliasProperty(_get_text,None,bind = ["msg"])