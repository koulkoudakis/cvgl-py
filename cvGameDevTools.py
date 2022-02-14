"""
Author: Sharome Burton
Date: 02/11/2022

"""
import cv2
import pygame

import HandTrackingModule as htm
import matrix

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def capture_frame():
    """

    :return:
    """
    screen = pygame.display.get_surface()
    capture = pygame.surfarray.pixels3d(screen)
    capture = capture.transpose([1, 0, 2])
    capture_bgr = cv2.cvtColor(capture, cv2.COLOR_RGB2BGR)
    return capture_bgr

class CvTool:
    def __init__(self, resW = 800, resH = 450, mat_size=(16, 9), max_hands=2):
        """

        :param resW:
        :param resH:
        :param mat_size:
        :param max_hands:
        """
        self.resW = resW
        self.resH = resH

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, resW)
        self.cap.set(4, resH)

        self.detector = htm.handDetector(mode=False, detectionCon=0.65, maxHands=max_hands)
        self.xp, self.yp = 0, 0

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.mat = matrix.PixMatrix(size=mat_size, img_size=(self.resH, self.resW, 3))

        self.drawColor = (255, 0, 255)
        self.brushThickness = 25

        self.wait = 1

    def key_input(self,  wait=1):
        """

        :param wait:
        :return:
        """
        if cv2.waitKey(self.wait) == ord('q'):
            self.end_prog(self.cap)
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

    def end_prog(self):
        """
        Exits program
        """
        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()

    def frame_step(self, face=False, display_face=True, display_eyes=False):
        """

        :param face:
        :param display_face:
        :param display_eyes:
        :return:
        """

        xp = None
        yp = None
        xf = None
        yf = None
        wf = None
        hf = None
        xcf = None
        ycf = None
        grid_row = None
        grid_col = None
        index_finger = False
        two_fingers = False

        key_pressed = self.key_input()

        if key_pressed == 's':
            self.mat.save_img()

        # mat.img = mat.img[:, :, :3]  # Channel 3

        _, frame = self.cap.read()
        frame = cv2.resize(frame, self.mat.img.shape[1::-1])
        frame = cv2.flip(frame, 1)

        # Grayscale each frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detects faces of different sizes in the input image
        if face:
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            print(faces, "\n")

            if display_face:
                for (x, y, w, h) in faces:
                    # To draw a rectangle on a face
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (230, 220, 210), 2)

                    # Using cv2.putText() method
                    img = cv2.putText(frame, 'face', (x, y - 5), self.font,
                                      1, (30, 220, 210), 2, cv2.LINE_AA)

                    if display_eyes:
                        # ROI for subface scanning
                        roi_gray = gray[y:y + h, x:x + w]
                        roi_color = img[y:y + h, x:x + w]

                        # Detects eyes of different sizes in the input image
                        eyes = eye_cascade.detectMultiScale(roi_gray)

                        # To draw a rectangle in eyes
                        for (ex, ey, ew, eh) in eyes:
                            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

            # Coordinates to return
            if len(faces) != 0:
                xf, yf, wf, hf = faces[0]
                xcf = xf + wf // 2
                ycf = yf + hf // 2

            face_inputs = [xf, yf, wf, hf, xcf, ycf]

        # 2. Find Hand Landmarks
        frame = self.detector.findHands(frame)
        lmList = self.detector.findPosition(frame, draw=False)

        if lmList != ([], (0, 0, 0, 0)) and len(lmList) != 0:
            x1, y1 = lmList[0][8][1:]
            x2, y2 = lmList[0][12][1:]

            # 3. Check which fingers are up
            fingers = self.detector.fingersUp()
            # print(fingers)

            # Index finger only up
            if fingers[1] and fingers[2] == False:
                index_finger = True
                cv2.circle(frame, (x1, y1), 15, self.drawColor, cv2.FILLED)
                print("Index Finger Mode")
                if self.xp == 0 and self.yp == 0:
                    xp, yp = x1, y1

                cv2.line(frame, (xp, yp), (x1, y1), self.drawColor, self.brushThickness)
                # cv2.line(mat.img, (xp, yp), (x1, y1), drawColor, brushThickness)
                grid_row, grid_col = self.mat.paint_fill_matrix(xp, yp, color = (123,123,123))

                # if drawColor == (0, 0, 0):
                #     cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

                # else:
                #     cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1

            # 4. Selection Mode - Two finger are up
            if fingers[1] and fingers[2]:
                two_fingers = True

                print("Two Finger Mode")

                frame = cv2.rectangle(frame, (x1, y1 - 25), (x2, y2 + 25), self.drawColor, cv2.FILLED)
                xp, yp = x1, y1
                grid_row, grid_col = self.mat.paint_fill_matrix(xp, yp, color=(123, 123, 123))

        # Finger inputs
        finger_inputs = (xp, yp, grid_row, grid_col, index_finger, two_fingers)

        # cv2.imshow('frame', frame)

        # print(frame.shape)
        # print(mat.img.shape)
        #
        # mat.img = mat.img[:, :, :3]  # Channel 3

        overlayed = cv2.addWeighted(frame, 0.5, self.mat.img, 0.5, 0)

        # cv2.imshow('mask', mask)
        # cv2.imshow('result', result)

        # cv2.imshow('overlayed', overlayed)

        # self.mat.show_img()

        # augment = cv2.bitwise_or(frame, frame, mask=mask)
        # cv2.imshow('augment', augment)
        # print(augment)

        # Wait for Esc key to stop
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            self.end_prog()

        if face:
            return frame, overlayed, self.mat.img, finger_inputs, face_inputs
        else:
            return frame, overlayed, self.mat.img, finger_inputs