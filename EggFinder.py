from Map import Map
from Egg import Egg
import numpy as np
from PIL import Image
from mss.windows import MSS as mss
import time
import json

GOLDEGGFULLARRAY = np.asarray(Image.open("res\\GoldEggFull.png"))
BLUEEGGFULLARRAY = np.asarray(Image.open("res\\BlueEggFull.png"))

maps=[{'name':"BQK", 'image':Image.open("res\\BQK.png")}]
#, {'name':"Helix", 'image':Image.open("res\\Helix.png")}, 
#{'name':"Nest", 'image':Image.open("res\\Nest.png")}, {'name':"Pod", 'image':Image.open("res\\Pod.png")}, 
#{'name':"Spire", 'image':Image.open("res\\Spire.png")}, {'name':"Split", 'image':Image.open("res\\Split.png")}, 
#{'name':"Tally", 'image':Image.open("res\\Tally.png")}]

for map in maps:
    map['array'] = np.asarray(map['image'])

for map in maps:
    blueLocs = []
    goldLocs = []
    for i in range(1920-BLUEEGGFULLARRAY.shape[1]):
        for ii in range(1080-BLUEEGGFULLARRAY.shape[0]):
            testArea = map['array'][ii:ii+BLUEEGGFULLARRAY.shape[0], i:i+BLUEEGGFULLARRAY.shape[1]]
            hits = np.sum(np.equal(BLUEEGGFULLARRAY, testArea))
            if (hits > BLUEEGGFULLARRAY.size * .75):
                    blueLocs.append({'x':i, 'y':ii})
    for i in range(1920-GOLDEGGFULLARRAY.shape[1]):
        for ii in range(1080-GOLDEGGFULLARRAY.shape[0]):
            testArea = map['array'][ii:ii+GOLDEGGFULLARRAY.shape[0], i:i+GOLDEGGFULLARRAY.shape[1]]
            hits = np.sum(np.equal(GOLDEGGFULLARRAY, testArea))
            if (hits > GOLDEGGFULLARRAY.size * .75):
                    goldLocs.append({'x':i, 'y':ii})
    map['blueEggs'] = blueLocs
    map['goldEggs'] = goldLocs
    del map['image']
    del map['array']
    print(map['name'] + ": Blue: " + str(len(blueLocs)))
    print(map['name'] + ": Gold: " + str(len(goldLocs)))
    with open("res\\" + map['name'] + " Eggs.json", 'w') as outfile:
        json.dump(map, outfile)

