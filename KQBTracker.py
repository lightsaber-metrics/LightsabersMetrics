from Map import Map
from Berry import Berry
from Set import Set
from Game import Game
import numpy as np
from PIL import Image
from mss.windows import MSS as mss
import time
import json
import os

BLUEWINARRAY = np.asarray(Image.open(os.path.join("res","BlueWins.png")))
GOLDWINARRAY = np.asarray(Image.open(os.path.join("res","GoldWins.png")))
ECONWINARRAY = np.asarray(Image.open(os.path.join("res","EconomicVictory.png")))
MILWINARRAY = np.asarray(Image.open(os.path.join("res","MilitaryVictory.png")))
SNAILWINARRAY = np.asarray(Image.open(os.path.join("res","SnailVictory.png")))
mapNames = ["BQK", "Helix", "Nest", "Pod", "Spire", "Split", "Tally"]
maps = []
mon = {"top": 0, "left": 0, "width": 1920, "height": 1080}
sct = mss()

def initMaps():
    for name in mapNames:
        maps.append(Map(name))   

def checkMap(state, confidenceReq = 60):
    currConfidence = 0
    currMap = ()
    for map in maps:
        hits = np.sum(np.equal(map.array, state))
        if (hits > currConfidence):
            currConfidence = hits
            currMap = map
    currConfidence = 100 * currConfidence / state.size
    if (currConfidence > confidenceReq):
        return currMap
    else:
        return None

def getScreen():
    sct_img = sct.grab(mon)
    img = Image.new("RGB", sct_img.size)
    pixels = zip(sct_img.raw[2::4], sct_img.raw[1::4], sct_img.raw[0::4])
    img.putdata(list(pixels))
    return np.asarray(img)

def parseEndScreen(state):
    winner = None
    condition = None
    blueHits = 0
    goldHits = 0 
    testArea = state[0:BLUEWINARRAY.shape[0], 628:628+BLUEWINARRAY.shape[1]]
    blueHits = np.sum(np.equal(testArea, BLUEWINARRAY))
    goldHits = np.sum(np.equal(testArea, GOLDWINARRAY))
    if (blueHits / testArea.size > .99):
        winner = "blue"
    else:
        if (goldHits / testArea.size > .99):
            winner = "gold"
    snailHits = 0
    milHits = 0
    ecoHits = 0
    testArea = state[1080-SNAILWINARRAY.shape[0]:1080, 546:546+SNAILWINARRAY.shape[1]]
    snailHits = np.sum(np.equal(testArea, SNAILWINARRAY))
    milHits = np.sum(np.equal(testArea, MILWINARRAY))
    ecoHits = np.sum(np.equal(testArea, ECONWINARRAY))
    if (snailHits / testArea.size > .99):
        condition = "snail"
    else:
        if (milHits / testArea.size > .99):
            condition = "military"
        else:
            if (ecoHits / testArea.size > .99):
                condition = "economy"
    if (winner is not None and condition is not None):
        return (winner, condition)
    return None


def startSet():
    currSet = Set()
    while (not currSet.complete):
        currMap = None
        print ("Waiting to detect game...")
        while (currMap is None):
            currScreen = getScreen()
            currMap = checkMap(currScreen)
        currGame = Game(currMap)
        print ("Map: " + currGame.map.name)
        mapChanged = False
        while (not mapChanged):
            mapChanged = currGame.update(getScreen())
        currWinner = None
        endTime = time.time()
        while (currWinner is None):
            currWinner = parseEndScreen(getScreen())
        currGame.endGame(currWinner[0], currWinner[1], endTime)
        print (currGame.getInfo())
        currSet.addGame(currGame)
        currSet.checkWinner()
    print (currSet.getInfo())
    currSet.toCSV()

if __name__ == '__main__':
    initMaps()
    for map in maps:
        print (map.name)
    while (True):
        startSet()
    print ("Exiting.")