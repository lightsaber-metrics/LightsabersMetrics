from Map import Map
from Berry import Berry
import numpy as np
from PIL import Image
from mss.windows import MSS as mss
import time
import json

EMPTYHOLEARRAY = np.asarray(Image.open("res\\EmptyBerry.png"))

maps=[{'name':"BQK", 'image':Image.open("BQK.png")}, {'name':"Helix", 'image':Image.open("Helix.png")}, 
{'name':"Nest", 'image':Image.open("Nest.png")}, {'name':"Pod", 'image':Image.open("Pod.png")}, 
{'name':"Spire", 'image':Image.open("Spire.png")}, {'name':"Split", 'image':Image.open("Split.png")}, 
{'name':"Tally", 'image':Image.open("Tally.png")}]

for map in maps:
    map['array'] = np.asarray(map['image'])

for map in maps:
    blueLocs = []
    goldLocs = []
    for i in range(1902):
        for ii in range(1066):
            testArea = map['array'][ii:ii+EMPTYHOLEARRAY.shape[0], i:i+EMPTYHOLEARRAY.shape[1]]
            hits = np.sum(np.equal(EMPTYHOLEARRAY, testArea))
            if (hits > 705):
                if (i<960):
                    blueLocs.append({'x':i, 'y':ii})
                else:
                    goldLocs.append({'x':i, 'y':ii})
    map['blueBerries'] = blueLocs
    map['goldBerries'] = goldLocs
    map['blueSnail'] = 0
    map['goldSnail'] = 0
    del map['image']
    del map['array']
    print(map['name'] + ": Blue: " + str(len(blueLocs)))
    print(map['name'] + ": Gold: " + str(len(goldLocs)))
    with open("res\\" + map['name'] + ".json", 'w') as outfile:
        json.dump(map, outfile)

