# Computer Vision Game Library (CVGL)

### Contributors:
* Sharome Burton
* Logan Abreo
* Cristiano Castaneda

![image](/img/logo.png)


[![CVGL advert](/img/yt.jpg)](https://www.youtube.com/watch?v=8n-QzCVP2iQ)


### The way too short but 100% accurate instructions

* Make sure the PC you're using has a camera (preferably front-facing). Device `0` in the line `cap = VideoCapture(0)` in `cvGameDevTools.py` usually refers to the front-facing camera. Use `1` as the argument to set to front-facing camera
* Install PyCharm or any other IDE that allows you to run Python natively on your PC (Python 3.9 ideally)
* `pip install` required librariesL `opencv-python`, `pygame`, `numpy`, `mediapipe`
* Try out demo implementations of CVGL with `tictactoe.py`, `snake.py`, `pong.py`, `spaceinvaders.py`, `spaceface.py`
* **Implementation in new games**: The jist of it is:
  - `import cvGameDevTools` *CVGL library
  - `import cv2` *openCV*
  - Instantiate `CvTool` object, passing in the window resolution of the game in question
  - Use `capture_frame()` from cvGameDevTools to capture game display as openCV compatible image
  - Use`frame_step()` from cvGameDevTools to return info such as hand, face and finger positions and gestures
  - Use info returned from `frame_step()` as you would any other keyboard or mouse input event.
  - A window with the camera video feed overlayed on the game screen will be automatically created

## Credit

### pyGame, OpenCV, mediapipe Tutorial Resources
- Coding with Russ
- Tech with Tim
- Murtaza's Workshop

#### Playtesters
- Eldon Pindell
- Carden Taylor
- Ezra Nyberg
- Joachim Isaac
- Sir Ruben
- Samuel Campbell
- Joshua (CS major)
- Christa (geoscience major)
- Mr. Carpenter (math major)
