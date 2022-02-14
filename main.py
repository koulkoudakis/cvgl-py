

import cv2
import numpy as np
import HandTrackingModule as htm

import matrix


# import game
# import tictactoe


resW = 800
resH = 450

cap = cv2.VideoCapture(0)
cap.set(3, resW)
cap.set(4, resH)

detector = htm.handDetector(mode=False, detectionCon=0.65, maxHands=1)
xp, yp = 0, 0
# imgCanvas = np.zeros((720, 1280, 3), np.uint8)

mat = matrix.PixMatrix(img_size=(resH, resW, 3))

drawColor = (255, 0, 255)
brushThickness = 25

def key_input(cap,  wait=1):
    if cv2.waitKey(wait) == ord('q'):
        end_prog(cap)
        return 'q'

    if cv2.waitKey(wait) == ord('w'):
        return 'w'

    if cv2.waitKey(wait) == ord('s'):
        return 's'

    if cv2.waitKey(wait) == ord('a'):
        return 'a'

    if cv2.waitKey(wait) == ord('d'):
        return 'd'

    return None

def end_prog(cap):
    """
    Exits program
    """
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

while True:
    key_pressed = key_input(cap)

    if key_pressed == 's':
        mat.save_img()

    # mat.img = mat.img[:, :, :3]  # Channel 3

    _, frame = cap.read()
    frame = cv2.resize(frame, mat.img.shape[1::-1])
    frame = cv2.flip(frame, 1)
    # It converts the BGR color space of image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # 90 57 100
    # Threshold of blue in HSV space
    lower_hsv = np.array([25, 75, 0])
    upper_hsv = np.array([55, 255, 255])

    # preparing the mask to overlay
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # The black region in the mask has the value of 0,
    # so when multiplied with original image removes all non-blue regions
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # 2. Find Hand Landmarks
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=True)

    if lmList != ([], (0, 0, 0, 0)) and len(lmList) != 0:
        x1, y1 = lmList[0][8][1:]
        x2, y2 = lmList[0][12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # Index finger only up
        if fingers[1] and fingers[2] == False:
            cv2.circle(frame, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            cv2.line(frame, (xp, yp), (x1, y1), drawColor, brushThickness)
            # cv2.line(mat.img, (xp, yp), (x1, y1), drawColor, brushThickness)
            mat.paint_fill_matrix(xp, yp)

            # if drawColor == (0, 0, 0):
            #     cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
            #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

            # else:
            #     cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

        # 4. Selection Mode - Two finger are up
        if fingers[1] and fingers[2]:
            # xp, yp = 0, 0
            print("Selection Mode")
            # # Checking for the click
            # if y1 < 125:
            #     if 250 < x1 < 450:
            #         header = overlayList[0]
            #         drawColor = (255, 0, 255)
            #     elif 550 < x1 < 750:
            #         header = overlayList[1]
            #         drawColor = (255, 0, 0)
            #     elif 800 < x1 < 950:
            #         header = overlayList[2]
            #         drawColor = (0, 255, 0)
            #     elif 1050 < x1 < 1200:
            #         header = overlayList[3]
            #         drawColor = (0, 0, 0)
            frame = cv2.rectangle(frame, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

    cv2.imshow('frame', frame)

    # print(frame.shape)
    # print(mat.img.shape)

    # mat.img = mat.img[:, :, :3]  # Channel 3
    overlayed = cv2.addWeighted(frame, 0.5, mat.img, 0.5, 0)
    # cv2.imshow('mask', mask)
    # cv2.imshow('result', result)
    cv2.imshow('overlayed', overlayed)
    mat.show_img()

    # augment = cv2.bitwise_or(frame, frame, mask=mask)
    # cv2.imshow('augment', augment)
    # print(augment)

    # Wait for Esc key to stop
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()