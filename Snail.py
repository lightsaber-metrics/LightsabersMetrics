import numpy as np
from PIL import Image
import os

class Snail:     

    snail = {'array':np.asarray(Image.open(os.path.join("res", "Snail.png")))}
    snail['xSize'] = snail['array'].shape[1]
    snail['ySize'] = snail['array'].shape[0]

    @classmethod
    def checkSnailLoc(cls, state, map):
        for height in map.snailHeights:
            for i in range (state.shape[1]-cls.snail['xSize']):
                testArea = state[height:height+cls.snail['ySize'], i:i+cls.snail['xSize']]
                hits = np.sum(np.equal(cls.snail['array'], testArea))
                if (hits > .9 * cls.snail['array'].size):
                    return i
        return None