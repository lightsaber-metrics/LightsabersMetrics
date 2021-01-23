from Game import Game as Game
from time import time
from datetime import datetime
import os
import csv

class Set:

    def __init__(self):
        self.games = []
        self.winner = ""
        self.complete = False
        self.blueWins = 0
        self.goldWins = 0

    def addGame(self, game):
        self.games.append(game)
        if (game.winner == "blue"):
            self.blueWins += 1
        else:
            self.goldWins +=1

    def log(self):
        now = datetime.now()
        f = open(os.path.join("logs", now.strftime("%m-%d-%Y - %H.%M.%S.log")), "x")
        toLog = ""
        for i in range(len(self.games)):
            toLog += "Game " + str(i+1) + ":\n"
            toLog += self.games[i].eventLog
        f.write(toLog)
        f.close()

    def checkWinner(self): 
        if (self.blueWins >= 3):
            self.complete = True
            self.winner = "blue"
            self.log()
            return self.winner
        else:
            if (self.goldWins >= 3):
                self.complete = True
                self.winner = "gold"
                self.log()
                return self.winner
        return None

    def getInfo(self):
        info = "Set Info:\n"
        if (self.winner is not None):
            info += "\tWinner: " + self.winner + "\n"
        info += "\tSet Count: Blue: " + str(self.blueWins) + " Gold: " + str(self.goldWins) +"\n"
        if (self.complete):
            totalTime = 0
            for game in self.games:
                totalTime += game.length
            info += "\tTotal Set Length: " + str(round(totalTime, 2)) + "\n"
        else:
            if (len(self.games) > 0):
                info += "\tTime Elapsed: " + str(round((time()-self.games[0].startTime), 2)) + "\n"
                info += "\tGame Info:\n"
        for game in self.games:
            info += game.getInfo()
        return info

    def toCSV(self):
        csv = "map,winner,win condition,blue queen lives,gold queen lives,blue berries in,gold berries in\n"
        for game in self.games:
            csv += game.map.name + "," + game.winner + "," + game.winCondition + "," + str(game.blueQueenLives) + "," + str(game.goldQueenLives) + "," + str(game.blueBerriesIn) + "," + str(game.goldBerriesIn) + "\n"
        now = datetime.now()
        f = open(os.path.join("logs", now.strftime("%m-%d-%Y - %H-%M-%S.csv")), "x")
        f.write(csv)
        f.close()