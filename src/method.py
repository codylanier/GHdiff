# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:44:09 2019

@author: codyl
"""

import chparse

with open('lostdream.chart') as chartfile:
    chart = chparse.load(chartfile)
print(chart.instruments[chparse.EXPERT][chparse.GUITAR][0])