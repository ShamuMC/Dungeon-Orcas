# -*- coding: utf-8 -*-
"""
Created on Tue May 17 09:35:04 2016

@author: SASedlacek
"""

from sqlalchemy import create_engine,MetaData,Table
from sqlalchemy.orm import mapper,sessionmaker 

db = create_engine("sqlite:///items/game.db")
metadata = MetaData(db)
class Items(object):
    pass
itemsdata = Table("Items",metadata,autoload = True)
mapper(Items,itemsdata)
Session = sessionmaker(bind = db)
session = Session()