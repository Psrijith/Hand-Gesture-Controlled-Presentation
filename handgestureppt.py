import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# variables
width, height = 1280, 720
folderPath = "Presentation"

# camera
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# get the list of presentation
pathImages = sorted(os.listdir(folderPath), key=len)

# variables
imgNumber = 0
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
annotations = [[]]
annotationNumber = 0
annotationStart = False

# Hand Detection
detector = HandDetector(detectionCon=0.8, maxHands=1)
gestureThreshold = 330

while True:
    # Import Images
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)
    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and not buttonPressed:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']

        lmList = hand['lmList']

        # constrained value for easy drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal

        if gestureThreshold >= cy:  # if the hand is above the line
            annotationStart = False
            # gesture 1 - left
            if fingers == [1, 0, 0, 0, 0]:
                #print("left")
                annotationStart = False
                if imgNumber > 0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNumber -= 1
            # gesture 2 - right
            if fingers == [0, 0, 0, 0, 1]:
                #print("right")
                annotationStart = False
                if imgNumber < len(pathImages) - 1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNumber += 1
        # Gesture 3 - show pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotationStart = False


        # Gesture 4 - Draw pointer
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])

            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart=False

        #gesture 5 - erase 
        if fingers == [1, 1, 1, 1, 1]:
            if annotations:
                if annotationNumber >= 0:
                    annotations.pop(-1)
                    annotationNumber-=1
                    buttonPressed = True
    else:
        annotationStart=False
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j!=0:
                cv2.line(imgCurrent,annotations[i][j-1],annotations[i][j],(0,0,200),12)


    # Resize the camera image for better visibility
    scale_percent = 60  # adjust the scale as needed
    width_scaled = int(img.shape[1] * scale_percent / 100)
    height_scaled = int(img.shape[0] * scale_percent / 100)
    img = cv2.resize(img, (width_scaled, height_scaled))

    # Get the dimensions of the scaled camera image
    h_cam, w_cam, _ = img.shape

    # Create an overlay image with the slides and scaled camera feed
    overlay = imgCurrent.copy()
    overlay[0:h_cam, -w_cam:] = img  # Place the scaled camera image at the top right corner
    overlay = cv2.resize(overlay, (int(width / 1.2), int(height / 1.2)))

    # Display the overlay
    cv2.imshow("slides", overlay)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
