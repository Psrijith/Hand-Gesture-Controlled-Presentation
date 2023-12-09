import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

width, height = 1280, 720

# Camera
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Variables
buttonPressed = False
annotations = [[]]
annotationNumber = 0
annotationStart = False
selectedColor = (0, 0, 255)  # default color

# Hand Detection
detector = HandDetector(detectionCon=0.8, maxHands=2)
gestureThreshold = 330

# Rules displayed on top left corner
rulesText = "Rules:\n"
rulesText += "- 3 fingers: Show pointer\n"
rulesText += "- 2 fingers pointing: Change color to pointed location\n"
rulesText += "- 5 fingers: Erase drawing\n"
rulesText += "- 1 finger & hold: Select color (click on desired color)"

# Color palette positions and colors
palette_positions = [
    (100, 100),  # red
    (200, 100),  # green
    (300, 100),  # blue
    (400, 100),  # yellow
    (500, 100),  # black
]
palette_colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (0, 0, 0)]

while True:
    # Import Images
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands:
        for hand in hands:
            fingers = detector.fingersUp(hand)
            cx, cy = hand['center']

            lmList = hand['lmList']

            # Constrained value for easy drawing
            xVal = int(np.interp(lmList[8][0], [0, width], [0, width]))
            yVal = int(np.interp(lmList[8][1], [0, height], [0, height]))
            indexFinger = xVal, yVal

            # Gesture 3 - show pointer
            if fingers == [0, 1, 1, 0, 0]:
                cv2.circle(img, indexFinger, 12, (0, 0, 255), cv2.FILLED)
                annotationStart = False

            # Gesture 2 fingers pointing - Change color to pointed location
            if fingers == [1, 1, 0, 0, 0]:
                # Check if pointing fingers are close to any color palette
                for i, (x, y) in enumerate(palette_positions):
                    if abs(x - indexFinger[0]) < 30 and abs(y - indexFinger[1]) < 30:
                        selectedColor = palette_colors[i]
                        buttonPressed = True
                        rulesText = f"Rules:\n- 3 fingers: Show pointer\n- 2 fingers pointing: Change color to {palette_colors[i]}\n- 5 fingers: Erase drawing\n- 1 finger & hold: Select color (click on desired color)"
                        break

            # Gesture 4 - Draw pointer with selected color
            if fingers == [0, 1, 0, 0, 0]:
                if annotationStart is False:
                    annotationStart = True
                    annotationNumber += 1
                    annotations.append([])

                cv2.circle(img, indexFinger, 12, selectedColor, cv2.FILLED)
                annotations[annotationNumber].append(indexFinger)
            else:
                annotationStart = False

            # One finger to select color
            if fingers == [0, 0, 0, 0, 0] and not buttonPressed:
                # Check if finger is inside any color palette
                for i, (x, y) in enumerate(palette_positions):
                    if x < indexFinger[0] < x + 50 and y < indexFinger[1] < y + 50:
                        selectedColor = palette_colors[i]
                        buttonPressed = True
                        rulesText = f"Rules:\n- 3 fingers: Show pointer\n- 2 fingers pointing: Change color to {palette_colors[i]}\n- 5 fingers: Erase drawing\n- 1 finger & hold: Select color (click on desired color)"
                        break

            # Gesture 5 - erase
            if fingers == [1, 1, 1, 1, 1]:
                if annotations:
                    if annotationNumber >= 0:
                        annotations.pop(-1)
                        annotationNumber -= 1
                        buttonPressed = True
            elif buttonPressed:
                buttonPressed = False

    # Draw annotations
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(img, annotations[i][j - 1], annotations[i][j], selectedColor, 12)

    # Draw color palette
    for i, (x, y) in enumerate(palette_positions):
        cv2.circle(img, (x, y), 25, palette_colors[i], cv2.FILLED)

    # Display rules text
    cv2.putText(img, rulesText, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # Display the image
    cv2.imshow('Hand Tracking', img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
