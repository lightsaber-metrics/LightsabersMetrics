import numpy as np
from PIL import Image
import os

class WinCon:
    winnerInfo = {'blueArray':np.asarray(Image.open(os.path.join("res","BlueWins.png"))), 
    'goldArray':np.asarray(Image.open(os.path.join("res","GoldWins.png"))), 'x':628, 'y':0}
    winnerInfo['xSize'] = winnerInfo['blueArray'].shape[1]
    winnerInfo['ySize']  = winnerInfo['blueArray'].shape[0]
    conditionInfo = {'snailArray':np.asarray(Image.open(os.path.join("res","SnailVictory.png"))),
    'milArray':np.asarray(Image.open(os.path.join("res","MilitaryVictory.png"))),
    'ecoArray':np.asarray(Image.open(os.path.join("res","EconomicVictory.png")))}
    conditionInfo['xSize'] = conditionInfo['snailArray'].shape[1]
    conditionInfo['ySize'] = conditionInfo['snailArray'].shape[0]
    conditionInfo['x'] = 546
    conditionInfo['y'] = 1080-conditionInfo['ySize']

    @classmethod
    def checkWinCon(cls, state):
        winner = None
        condition = None
        winnerArea = state[cls.winnerInfo['y']:cls.winnerInfo['y']+cls.winnerInfo['ySize'], cls.winnerInfo['x']:cls.winnerInfo['x']+cls.winnerInfo['xSize']]
        blueHits = np.sum(np.equal(winnerArea, cls.winnerInfo['blueArray']))
        goldHits = np.sum(np.equal(winnerArea, cls.winnerInfo['goldArray']))
        if (blueHits / winnerArea.size > .99):
            winner = "blue"
        else:
            if (goldHits / winnerArea.size > .99):
                winner = "gold"
        conditionArea = state[cls.conditionInfo['y']:cls.conditionInfo['y']+cls.conditionInfo['ySize'], cls.conditionInfo['x']:cls.conditionInfo['x']+cls.conditionInfo['xSize']]
        snailHits = np.sum(np.equal(conditionArea, cls.conditionInfo['snailArray']))
        milHits = np.sum(np.equal(conditionArea, cls.conditionInfo['milArray']))
        ecoHits = np.sum(np.equal(conditionArea, cls.conditionInfo['ecoArray']))
        if (snailHits / conditionArea.size > .99):
            condition = "snail"
        else:
            if (milHits / conditionArea.size > .99):
                condition = "military"
            else:
                if (ecoHits / conditionArea.size > .99):
                    condition = "economy"
        if (winner is not None and condition is not None):
            return (winner, condition)
        return None
            

