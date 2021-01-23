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

class LSM:
    
    def __init__(self, modules = ["stats"]):
        self.modules = modules
        self.loop = True
    
    def freeze(self):
        while self.loop:
            print ("looping!")

    def stop(self):
        self.loop = False