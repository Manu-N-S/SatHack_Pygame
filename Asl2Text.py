import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Models/keras_model.h5", "Models/labels.txt")

offset = 20
imgSize = 300

# folder = "Data/C"
counter = 0

NumFrames=0
pLetter=""
cLetter=""
word =""

labels = ["A","B","c","D","E","F","G","H","A","J","K","L","M","N","O","P","N","R","S","T","U","V","W","X","Y","Z"]

def detect(img,flag):
    global pLetter,cLetter,NumFrames,word,counter,offset,imgSize

    if flag:
        word=''
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            print(prediction, index)
            cLetter = labels[index]
            if cLetter == pLetter:
                NumFrames = NumFrames+1
                print("FRAMES = ")
                print(NumFrames)
                print("\nCurrentLetter = ")
                print(cLetter)
                print("\nPreviousLetter = ")
                print(pLetter)
                if(NumFrames>=10):
                    word+=cLetter
                    text = word
                    engine.say(text)
                    engine.runAndWait()
                    NumFrames=0
                else:
                    pLetter=cLetter
                print("word is = "+word)
            else:
                pLetter=cLetter
                NumFrames=0
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

        # cv2.rectangle(imgOutput, (x - offset, y - offset-50),
        #               (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], ((y + h+offset)-(y-offset), x + w+offset+10), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x-offset, y-offset),
                      (x + w+offset, y + h+offset), (0, 0, 255), 4)


        #cv2.imshow("ImageCrop", imgCrop)
        #cv2.imshow("ImageWhite", imgWhite)
    return imgOutput,word
    # cv2.imshow("Image", imgOutput)
    # cv2.waitKey(1)