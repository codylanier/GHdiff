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
def isTChimney(note):
    if len(note) < 6:
        return False
    return note[0] > note[1] and note[1] < note[2] and note[2] < note[3] and note[4] == note[2] and note[5] == note[1]

def isQuadChimney(note):
    if len(note) < 8:
        return False
    return note[0] > note[1] and note[1] < note[2] and note[2] < note[3] and note[3] < note[4] and note[5] == note[3] and note[6] == note[2] and note[7] == note[1]

def isQuintChimney(note):
    if len(note) < 10:
        return False
    return note[0] > note[1] and note[1] < note[2] and note[2] < note[3] and note[3] < note[4] and note[4] < note[5] and note[6] == note[4] and note[7] == note[3] and note[8] == note[2] and note[9] == note[1]

#%%Reverse Chimney Detection
def isTReverseChimney(note):
    if len(note) < 6:
        return False
    return note[0] < note[1] and note[1] > note[2] and note[2] > note[3] and note[4] == note[2] and note[5] == note[1]

def isQReverseChimney(note):
    if len(note) < 8:
        return False
    return note[0] < note[1] and note[1] > note[2] and note[2] > note[3] and note[3] > note[4] and note[5] == note[3] and note[6] == note[2] and note[7] == note[1]
    pass

def isQuintReverseChimney(note):
    if len(note) < 10:
        return False
    return note[0] < note[1] and note[1] > note[2] and note[2] > note[3] and note[3] > note[4] and note[4] > note[5] and note[6] == note[4] and note[7] == note[3] and note[8] == note[2] and note[9] == note[1]
    pass

#%%Trip Detection
def isAscTrip(note):
    if len(note) < 3:
        return False
    return note[0] < note[1] and note[1] < note[2]

def isDscTrip(note):
    if len(note) < 3:
        return False
    return note[0] > note[1] and note[1] > note[2]

#%% Quad Detection
def isAscQuad(note):
    if len(note) < 4:
        return False
    return note[0] < note[1] and note[1] < note[2] and note[2] < note[3]

def isDscQuad(note):
    if len(note) < 4:
        return False
    return note[0] > note[1] and note[1] > note[2] and note[2] > note[3]

#%%Quint Detection
def isAscQuint(note):
    if len(note) < 5:
        return False
    return note[0] < note[1] and note[1] < note[2] and note[2] < note[3] and note[3] < note[4]

def isDscQuint(note):
    if len(note) < 5:
        return False
    return note[0] > note[1] and note[1] > note[2] and note[2] > note[3] and note[3] > note[4]
#%%Zig Detection
def isZig(note):
    if len(note) < 4:
        return False
    return note[0] < note[1] and note[1] < note[2] and note[3] == note[1]

def isQuadZig(note):
    if len(note) < 6:
        return False
    return note[0] < note[1] and note[1] < note[2] and note[2] < note[3] and note[4] == note[2] and note[5] == note[1]

def isQuintZig(note):
    if len(note) < 8:
        return False
    return note[0] < note[1] and note[1] < note[2] and note[2] < note[3] and note[3] < note[4] and note[5] == note[3] and note[6] == note[2] and note[7] == note[1]

def isUpNote(note):
    methodnotecount = 2
    return note[0] < note[1]

def isDownNote(note):
    methodnotecount = 2
    return note[0] > note[1]

#%%Other Detection
def isStrum(note): #will change
    methodnotecount = 2
    return note[0] == note[1]

def isChord(note):
    return len(note) > 1

def isHOPO(notes): #will change
    return not isStrum(notes)


def methodgrouper(fretdict):     
    '''
    designed to detect zig zags in numbers, not quite working correctly yet
    will probably become deprecated soon
    '''
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
        
def printchart(notes): #this is the best function in this entire script
    for note in (notes[::-1]):
        notestring = '- - - - -'
        lns = list(notestring)
        for fret in note:
            lns[2 * fret] = 'O'
        print(''.join(lns))
        
#%% add notes to a dictionary cooresponding to their tick number, and group chords together
def getFretDict(chart):
    fretarray = {}
    for note in xg:
        try:
            if fretarray.get(note.time, -1) == -1:
                fretarray[note.time] = [note.fret]
            else:
                fretarray[note.time] += [note.fret]
        except Exception:
            pass
    return fretarray

#%% get dictionary of BPM events and tick numbers
def getBPMDict(chart):
    sync = chart.sync_track
    bpmarray = {}
    for bpm in sync:
        if bpm.kind.value == 'B':
            bpmarray[bpm.time] = bpm.value / 1000
        
#%%calculate song length
def calcsonglength(chart):
    bpmdictionary = getBPMDict(chart)
    fretarray = getFretDict(chart)
    bpmarray = bpmdictionary
    bpmlocs = list(bpmarray.keys())
    songlength = 0
    for k in range(len(bpmlocs) - 1):
        ticklength = bpmlocs[k+1] - bpmlocs[k]
        songlength += tickstoseconds(ticklength, bpmarray[bpmlocs[k]])
    songlength += tickstoseconds(max(fretarray.keys()) - max(bpmlocs), bpmarray[max(bpmlocs)])
    return songlength

def interpretchart(chart):
    fretDict = getFretDict(chart)
    fretList = list(fretDict.values())
    methodList = []
    methodnotecount = 0
    while len(fretList) > 1:
        if len([fretList[0]]) > 1:
            methodList.append('Chord')
            methodnotecount = 1
        elif isQuintChimney(fretList):
            methodList.append('Quint Chimney')
            methodnotecount = 10
        elif isQuintReverseChimney(fretList):
            methodList.append('Quint Reverse Chimney')
            methodnotecount = 10
        elif isQuadChimney(fretList):
            methodList.append('Quad Chimney')
            methodnotecount = 8
        elif isQReverseChimney(fretList):
            methodList.append('Quad Reverse Chimney')
            methodnotecount = 8
        elif isQuintZig(fretList):
            methodList.append('Quint Zig')
            methodnotecount = 8
        elif isTChimney(fretList):
            methodList.append('Chimney')
            methodnotecount = 6
        elif isTReverseChimney(fretList):
            methodList.append('Reverse Chimney')
            methodnotecount = 6
        elif isQuadZig(fretList):
            methodList.append('Quad Zig')
            methodnotecount = 6 
        elif isAscQuint(fretList):
            methodList.append('Asc Quint')
            methodnotecount = 5
        elif isDscQuint(fretList):
            methodList.append('Dsc Quint')
            methodnotecount = 5 
        elif isAscQuad(fretList):
            methodList.append('Asc Quad')
            methodnotecount = 4
        elif isDscQuad(fretList):
            methodList.append('Dsc Quad')
            methodnotecount = 4
        elif isZig(fretList):
            methodList.append('Zig')
            methodnotecount = 4
        elif isAscTrip(fretList):
            methodList.append('Asc Trip')
            methodnotecount = 3
        elif isDscTrip(fretList):
            methodList.append('Dsc Trip')
            methodnotecount = 3
        elif isUpNote(fretList):
            methodList.append('Up')
            methodnotecount = 2
        elif isDownNote(fretList):
            methodList.append('Down')
            methodnotecount = 2
        else:
            methodList.append('Strum')
            methodnotecount = 1
        
        for k in range(methodnotecount):
            fretList.pop(0)
    return methodList
#%% import chart
with open('notes.chart', encoding=('utf-8-sig')) as chartfile:
    chart = chparse.parse.load(chartfile)
xg = chart.instruments[chparse.EXPERT][chparse.GUITAR]
chartlength = len(xg)


#%% printing diagnostincs
#print(fretarray)
#print(bpmarray)
#methodlist = methodgrouper(fretarray)
#print(methodlist)
fretarray = getFretDict(xg)
printchart(list(fretarray.values()))
print(interpretchart(xg))
#diff = len(methodlist) / songlength