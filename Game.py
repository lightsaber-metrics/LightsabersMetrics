from Berry import Berry
from WinCon import WinCon
from Egg import Egg
from Snail import Snail
from time import time
import numpy as np

class Game:

    def __init__(self, map, scoreboardKey=None):
        self.map = map
        self.winner = None
        self.winCondition = None
        self.startTime = time()
        self.length = None
        self.blueBerriesIn = 0
        self.goldBerriesIn = 0
        self.blueBerries = []
        self.snailLoc = 964
        for hole in self.map.blueHoles:
            self.blueBerries.append(Berry(hole[0], hole[1], "blue"))
        self.goldBerries = []
        for hole in self.map.goldHoles:
            self.goldBerries.append(Berry(hole[0], hole[1], "gold"))
        self.blueEggs = []
        for eggLoc in self.map.blueEggLocs:
            self.blueEggs.append(Egg(eggLoc[0], eggLoc[1], color="blue", map=self.map.name))
        self.goldEggs = []
        for eggLoc in self.map.goldEggLocs:
            self.goldEggs.append(Egg(eggLoc[0], eggLoc[1], color="gold", map=self.map.name))
        self.blueQueenLives = 3
        self.goldQueenLives = 3
        self.complete = False
        self.scoreboardKey = scoreboardKey
        self.eventLog = "Game Start. Map: " + self.map.name + " Local time: " + str(round(time(), 2)) + "\n"

    def log(self, message, currTime=None):
        if (currTime is None):
            currTime = time()
        toLog = str(round(currTime - self.startTime, 2)) + "s\t" + message
        print (toLog)
        self.eventLog += toLog + "\n"

    def updateSnail(self, state):
        currSnailLoc = Snail.checkSnailLoc(state=state, map=self.map)
        if currSnailLoc is not None and currSnailLoc != self.snailLoc:
            self.log("Snail Location: " + str(currSnailLoc))
            self.snailLoc = currSnailLoc
    
    def endGame (self, winner, winCondition, endTime=time()):
        self.complete = True
        self.winner = winner
        self.winCondition = winCondition
        self.length = endTime - self.startTime
        if (self.winCondition == "economy"):
            if (self.winner == "blue"):
                if (self.blueBerriesIn < 12):
                    self.blueBerriesIn = 12
                    self.log ("Blue Berries in: 12", endTime)
            else:
                if (self.goldBerriesIn < 12):
                    self.goldBerriesIn = 12
                    self.log ("Gold Berries in: 12")
        if (self.winCondition == "military"):
            if (self.winner == "blue"):
                self.goldQueenLives = 0
                self.log("Gold Queen Lives: 0", endTime)
            else:
                self.blueQueenLives = 0  
                self.log("Blue Queen Lives: 0", endTime)
        self.log("Game Over. " + self.winner.capitalize() + " wins!  Condition: " + self.winCondition.capitalize(), endTime)

    def updateBerries (self, state):
        currBlueBerriesIn = 0
        currGoldBerriesIn = 0
        for b in self.blueBerries:
            if (b.update(state)):
                currBlueBerriesIn += 1
        for b in self.goldBerries:
            if (b.update(state)):
                currGoldBerriesIn += 1
        if (not currBlueBerriesIn == self.blueBerriesIn):
            self.log("Blue Berries in: " + str(currBlueBerriesIn))
        if (not currGoldBerriesIn == self.goldBerriesIn):
            self.log("Gold Berries in: " + str(currGoldBerriesIn))
        self.blueBerriesIn = currBlueBerriesIn
        self.goldBerriesIn = currGoldBerriesIn
        return (self.blueBerriesIn, self.goldBerriesIn)

    def checkMapOver(self, state, confidenceReq = .6):
        hits = np.sum(np.equal(self.map.array, state))
        if ((hits / state.size) > confidenceReq):
            return False
        else:
            return True

    def update(self, state):
        self.updateQueenLives(state)
        self.updateBerries(state)
        self.updateSnail(state)
        return (WinCon.checkGameOver(state))

    def updateQueenLives(self, state):
        currBlueQueenLives = 1
        currGoldQueenLives = 1
        for blueEgg in self.blueEggs:
            if(blueEgg.update(state)):
                currBlueQueenLives += 1
        for goldEgg in self.goldEggs:
            if(goldEgg.update(state)):
                currGoldQueenLives += 1
        if (not currBlueQueenLives == self.blueQueenLives):
            self.log("Blue Queen Lives: " + str(currBlueQueenLives))
        if (not currGoldQueenLives == self.goldQueenLives):
            self.log("Gold Queen Lives: " + str(currGoldQueenLives))
        self.blueQueenLives = currBlueQueenLives
        self.goldQueenLives = currGoldQueenLives
        return (self.blueQueenLives, self.goldQueenLives)

    def getInfo (self):
        info = "Map: " + self.map.name + "\n"
        if (self.winner is not None):
            info += "\tWinner: " + self.winner + "\n"
        if (self.winCondition is not None):
            info += "\tWin Condition: " + self.winCondition + "\n"
        if (self.length is not None):
            info += "\tGame Length: " + str(round(self.length, 2)) +"\n"
        else:
            info += "\tTime Elapsed: " + str(round((time()-self.startTime),2))
        info += "\tBlue Berries: " + str(self.blueBerriesIn) + "\n"
        info += "\tGold Berries: " + str(self.goldBerriesIn) + "\n"
        return info