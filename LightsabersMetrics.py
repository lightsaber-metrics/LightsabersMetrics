from Map import Map
from Berry import Berry
from Set import Set
from Game import Game
from WinCon import WinCon
import numpy as np
from PIL import Image
from mss.windows import MSS as mss
import time
import json
import os

class LSM:
    
    def __init__(self, modules = ["stats", "logging"], scoreboardKey = None):
        mapNames = ["BQK", "Helix", "Nest", "Pod", "Spire", "Split", "Tally"]
        self.maps = []
        for name in mapNames:
            self.maps.append(Map(name))
        self.mon = {"mon":0, "top": 0, "left": 0, "width": 1920, "height": 1080}
        self.sct = mss()
        self.state = None
        self.currSet = None
        self.stats = "stats" in modules
        self.logging = "logging" in modules
        self.textFiles = "streamer" in modules
        self.scoreboard = "scoreboard" in modules
        self.scoreboardKey = scoreboardKey
        self.exit = False

    def stop(self):
        self.exit = True

    def updateState(self):
        sct_img = self.sct.grab(self.mon)
        img = Image.new("RGB", sct_img.size)
        pixels = zip(sct_img.raw[2::4], sct_img.raw[1::4], sct_img.raw[0::4])
        img.putdata(list(pixels))
        self.state = np.asarray(img)
        return self.state

    def startSet(self):
        self.currSet = Set()
        while (not self.currSet.complete):
            if self.exit:
                return
            currMap = None
            print ("Waiting to detect game...")
            while (currMap is None):
                currMap = Map.checkMap(maps = self.maps, state=self.updateState())
                if self.exit:
                    return
            currGame = Game(currMap, self.scoreboardKey)
            print ("Detected: " + currGame.map.name)
            while (not currGame.update(self.updateState())):
                if self.exit:
                    return
            currWinner = None
            endTime = time.time()
            while (currWinner is None):
                currWinner = WinCon.checkWinCon(self.updateState())
                if self.exit:
                    return
            currGame.endGame(currWinner[0], currWinner[1], endTime)
            self.currSet.addGame(currGame)
            self.currSet.checkWinner()
        if (self.stats):
            self.currSet.toCSV()
        if (self.logging):
            self.currSet.log()

    def record(self):
        while not self.exit:
            self.startSet()

if __name__ == '__main__':
    LSM = LSM()
    LSM.record()