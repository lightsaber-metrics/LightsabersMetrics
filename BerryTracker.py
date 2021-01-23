from mss.windows import MSS as mss
import numpy as np
import time
import cv2
from PIL import Image

maps=[{'name':"BQK", 'image':Image.open("BQK.png")}, {'name':"Helix", 'image':Image.open("Helix.png")}, 
{'name':"Nest", 'image':Image.open("Nest.png")}, {'name':"Pod", 'image':Image.open("Pod.png")}, 
{'name':"Spire", 'image':Image.open("Spire.png")}, {'name':"Split", 'image':Image.open("Split.png")}, 
{'name':"Tally", 'image':Image.open("Tally.png")}]
for map in maps:
    map['array'] = np.asarray(map['image'])

def findMap(img):
    currConfidence = 0
    currMap = "None"
    for map in maps:
        hits = np.sum(map['array']==img)
        if (hits > currConfidence):
            currConfidence = hits
            currMap = map['name']
    currConfidence = 100 * currConfidence / img.size
    if (currConfidence > 60):
        return (currMap, currConfidence)
    else:
        return ("idk", 0)

if __name__ == '__main__':
    mon = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    sct = mss()
    input("paused")
    last_time = time.time()
    while time.time() - last_time < 5:
        1+1
    print("Recording!")
    while (True):
        sct_img = sct.grab(mon)
        img = Image.new("RGB", sct_img.size)
        pixels = zip(sct_img.raw[2::4], sct_img.raw[1::4], sct_img.raw[0::4])
        img.putdata(list(pixels))
        imgArray = np.asarray(img)
        actualMap = findMap(imgArray)
        if (not actualMap[0] == "idk"):
            print("You are on " + actualMap[0] +" with confidence " + str(actualMap[1]) + "%")