import numpy as np
from PIL import Image
import os

class Berry:

    def __init__(self, x, y, color, filled=False):
        self.x = x
        self.y = y
        self.color = color
        self.filled = filled
        self.FULLARRAY = np.asarray(Image.open(os.path.join("res","FilledBerry.png")))
        self.EMPTYARRAY = np.asarray(Image.open(os.path.join("res","EmptyBerry.png")))
        self.ySize = self.FULLARRAY.shape[0]
        self.xSize = self.FULLARRAY.shape[1]

    def update(self, state):
        hits = 0
        testArea = state[self.y:self.y+self.ySize, self.x:self.x+self.xSize]
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