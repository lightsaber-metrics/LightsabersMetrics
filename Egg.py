import numpy as np
from PIL import Image
import os

class Egg:

    def __init__(self, x, y, color, map, filled=True):
        self.x = x
        self.y = y
        self.color = color
        self.filled = filled
        self.map = map
        self.FULLARRAY = np.asarray(Image.open(os.path.join("res","eggs", self.map+self.color+"full.png")))
        self.EMPTYARRAY = np.asarray(Image.open(os.path.join("res","eggs", self.map+self.color+"empty.png")))
        self.YSIZE = self.FULLARRAY.shape[0]
        self.XSIZE = self.FULLARRAY.shape[1]
        
    def update(self, state):
        hits = 0
        testArea = state[self.y:self.y+self.YSIZE, self.x:self.x+self.XSIZE]
        if (self.filled):
            hits = np.sum(np.equal(self.EMPTYARRAY, testArea))
            if (hits > .75 * self.EMPTYARRAY.size):
                self.filled = False
                return False
            else:
                return True
        else:
            hits = np.sum(np.equal(self.FULLARRAY, testArea))
            if (hits > .75 * self.FULLARRAY.size):
                self.filled = True
                return True
            else:
                return False