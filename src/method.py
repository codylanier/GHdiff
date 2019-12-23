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

#%%Chimney Detection
def isTChimney(notes):
    pass

def isQuadChimney(notes):
    pass

def isQuintChimney(notes):
    pass

#%%Reverse Chimney Detection
def isTReverseChimney(notes):
    pass  

def isQReverseChimney(notes):
    pass

def isQuintReverseChimney(notes):
    pass

#%%Trip Detection
def isAscTrip(notes):
    return note[0] < note[1] and note[1] < note[2]

def isDscTrip(notes):
    return note[0] > note[1] and note[1] > note[2]

#%% Quad Detection
def isAscQuad(notes):
    return note[0] < note[1] and note[1] < note[2] and note[2] < note[3]

def isDscQuad(notes):
    return note[0] > note[1] and note[1] > note[2] and note[2] > note[3]

#%%Quint Detection
def isAscQuint(notes):
    return note[0] < note[1] and note[1] < note[2] and note[2] < note[3] and note[3] < note[4]

def isDscQuint(notes):
    return note[0] > note[1] and note[1] > note[2] and note[2] > note[3] and note[3] > note[4]
#%%Zig Detection
def isZig(notes):
    return note[0] < note[1] and note[1] < note[2] and note[3] == note[1]

def isQuadZig(notes):
    return note[0] < note[1] and note[1] < note[2] and note[2] < note[3] and note[4] == note[2] and note[5] == note[1]

def isQuintZig(notes):
    return note[0] < note[1] and note[1] < note[2] and note[2] < note[3] and note[3] < note[4] and note[5] == note[3] and note[6] == note[2] and note[7] == note[1]

#%%Other Detection
def isStrum(notes):
    pass

def isHOPO(notes):
    pass


def methodgrouper(fretdict):     #designed to detect zig zags in numbers, not quite working correctly yet
    #will probably become deprecated soon
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