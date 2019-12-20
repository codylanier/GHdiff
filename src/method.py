# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:44:09 2019

@author: codyl
"""

def tickstoseconds(ticks, bpm):
    return None

#%% import chart
import chparse
with open('notes.chart', encoding=('utf-8-sig')) as chartfile:
    chart = chparse.parse.load(chartfile)
xg = chart.instruments[chparse.EXPERT][chparse.GUITAR]
chartlength = len(xg)
#print(xg)

#%% get dictionary of BPM events and tick numbers
sync = chart.sync_track
bpmarray = {}
for bpm in sync:
    if bpm.kind.value == 'B':
        if bpmarray.get(bpm.time, -1) == -1:
            bpmarray[bpm.time] = [bpm.value / 1000]
        else:
            bpmarray[bpm.time] += [bpm.value / 1000] #catch all just in case, this should be unused though
            
#%% add notes to a dictionary cooresponding to their tick number, and group chords together
fretarray = {}
for note in xg:
    if note.kind.value == 'N':
        if fretarray.get(note.time, -1) == -1:
            fretarray[note.time] = [note.fret]
        else:
            fretarray[note.time] += [note.fret]

#%%calcs


#%% printing diagnostincs
print(fretarray)
print(bpmarray)