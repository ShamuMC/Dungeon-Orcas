# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 14:01:24 2016

@author: gray
"""

class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__