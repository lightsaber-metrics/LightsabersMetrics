from PIL import Image
import numpy as np
import json
from Berry import Berry
from Egg import Egg
import os

class Map:
    def __init__(self, mapName):
        self.blueHoles = []
        self.goldHoles = []
        self.blueEggLocs = []
        self.goldEggLocs = []
        rawjson = json.load(open(os.path.join("res", mapName+".json")))
        self.name = rawjson['name']
        self.image = Image.open(os.path.join("res", mapName+".png"))
        self.array = np.asarray(self.image)
        for hole in rawjson['blueBerries']:
            self.blueHoles.append((hole['x'],hole['y']))
        for hole in rawjson['goldBerries']:
            self.goldHoles.append((hole['x'],hole['y']))
        for eggLoc in rawjson['blueEggs']:
            self.blueEggLocs.append((eggLoc['x'],eggLoc['y']))
        for eggLoc in rawjson['goldEggs']:
            self.goldEggLocs.append((eggLoc['x'],eggLoc['y']))
        self.blueSnail = rawjson['blueSnail']
        self.goldSnail = rawjson['goldSnail']

        