# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:44:09 2019

@author: codyl
"""

import chparse


def tickstoseconds(ticks, bpm):
    return ticks / 192 * 60 / bpm  #192 ticks per beat divided by beats per second
                                    #this is hardcoded to the resolution, may need to pull from metadata of the song

#%% import chart
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
        bpmarray[bpm.time] = bpm.value / 1000
            
#%% add notes to a dictionary cooresponding to their tick number, and group chords together
fretarray = {}
for note in xg:
    if note.kind.value == 'N':
        if fretarray.get(note.time, -1) == -1:
            fretarray[note.time] = [note.fret]
        else:
            fretarray[note.time] += [note.fret]

#%%calculate song length
bpmlocs = list(bpmarray.keys())
songlength = 0
for k in range(len(bpmlocs) - 1):
    bpmlength = bpmlocs[k+1] - bpmlocs[k]
    songlength += tickstoseconds(bpmlength, bpmarray[bpmlocs[k]])
songlength += tickstoseconds(max(fretarray.keys()) - max(bpmlocs), bpmarray[max(bpmlocs)])
#%% printing diagnostincs
print(fretarray)
print(bpmarray)
print(songlength)