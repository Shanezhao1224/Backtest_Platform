# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 18:56:05 2020

@author: Xzhao
"""
from Order_class import Order

class BOSC:
    
    def __init__(self):
        pass

    def open(self,curropen,balance,shares_cur):
        shares = int(balance / curropen)
        order = Order(True,shares)
        return order
    
    def close(self,currclose, balance,shares_cur):
        order = Order(False,shares_cur)
        return order



        
