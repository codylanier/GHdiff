# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:44:09 2019

@author: codyl
"""

import chparse
import numpy as np

def tickstoseconds(ticks, bpm):
    return ticks / 192 * 60 / bpm  #192 ticks per beat divided by beats per second
                                    #this is hardcoded to the resolution, may need to pull from metadata of the song
                                    
def methodgrouper(fretdict):     #designed to detect zig zags in numbers, not quite working correctly yet
    notearray = list(fretarray.values())
    methodlist = []
    methodinst = []
    prevnote = -1
    top = True
    for note in notearray:
        endgroup = True
        if len(note) == 1:
            if note[0] > prevnote and top: 
                methodinst += note
                endgroup = False
            elif note[0] < prevnote:
                methodinst += note
                endgroup = False
                top = False
        if endgroup:
            methodlist += [methodinst]
            methodinst = note
        prevnote = note[0]
    return methodlist
        
#%% import chart
with open('lostdream.chart', encoding=('utf-8-sig')) as chartfile:
    chart = chparse.parse.load(chartfile)
xg = chart.instruments[chparse.EXPERT][chparse.GUITAR]
chartlength = len(xg)
#print(xg)

#%% get dictionary of BPM events and tick numbers
sync = chart.sync_track
bpmarray = {}
for bpm in sync:
    if bpm.kind.value == 'B':
        bpmarray[bpm.time] = bpm.value / 1000
            
#%% add notes to a dictionary cooresponding to their tick number, and group chords together
fretarray = {}
for note in xg:
    try:
        if fretarray.get(note.time, -1) == -1:
            fretarray[note.time] = [note.fret]
        else:
            fretarray[note.time] += [note.fret]
    except Exception:
        pass
#%%calculate song length
bpmlocs = list(bpmarray.keys())
songlength = 0
for k in range(len(bpmlocs) - 1):
    ticklength = bpmlocs[k+1] - bpmlocs[k]
    songlength += tickstoseconds(ticklength, bpmarray[bpmlocs[k]])
songlength += tickstoseconds(max(fretarray.keys()) - max(bpmlocs), bpmarray[max(bpmlocs)])

#%% printing diagnostincs
#print(fretarray)
#print(bpmarray)
methodlist = methodgrouper(fretarray)
print(methodlist)

diff = len(methodlist) / songlength