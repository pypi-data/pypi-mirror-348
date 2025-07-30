#CoinCombo.py
from radboy.DB.db import *
from radboy.FB.FormBuilder import *
from radboy.FB.FBMTXT import *
from radboy.DB.Prompt import *
from radboy.DB.Prompt import prefix_text
import pandas as pd
from datetime import date,datetime
import calendar
import plotext as plt
import numpy as np
from radboy.BNC.BnC import *
import tarfile
import uuid


class CoinCombo4TTL(BASE,Template):
    __tablename__="CoinCombo4TTL"
    cc4ttlid=Column(Integer,primary_key=True)
    Calculated_Total=Column(Float,default=round(0,2))
    TTL=Column(Float,default=round(0,2))
    DTOE=Column(DateTime,default=datetime.now())
    CurrencyName=Column(String,default='')
    CurrencyValue=Column(Float,default=round(0,2))
    CurrencyNeeded4TTL=Column(Integer,default=0)

    group_id=Column(String,default=str(uuid.uuid1()))

    def __init__(self,**kwargs):
        for k in kwargs.keys():
            if k in [s.name for s in self.__table__.columns]:
                setattr(self,k,kwargs.get(k))

try:
    CoinCombo4TTL.metadata.create_all(ENGINE)
except Exception as e:
    print(e)
    CoinCombo4TTL.metadata.drop(ENGINE)
    CoinCombo4TTL.metadata.create_all(ENGINE)   