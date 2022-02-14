# Computer Vision Game Library (CVGL)

<p align="center">
  <img width="300" height="300" src="/img/logo.png">
</p>


<!-- ![image](/img/logo.png) -->

[![CVGL advert](/img/yt.jpg)](https://www.youtube.com/watch?v=8n-QzCVP2iQ)
<p align="center">
<!--   <img width="200" height="200" src="/img/yt.jpg" a href="https://www.youtube.com/watch?v=8n-QzCVP2iQ">
</p> -->

### Contributors:
* Sharome Burton
* Logan Abreo
* Cristiano Castaneda

### The way too short but 100% accurate instructions

* Make sure the PC you're using has a camera (preferably front-facing). Device `0` in the line `cap = VideoCapture(0)` in `cvGameDevTools.py` usually refers to the front-facing camera. Use `1` as the argument to set to front-facing camera
* Install PyCharm or any other IDE that allows you to run Python natively on your PC (Python 3.9 ideally)
* `pip install` required libraries: `opencv-python`, `pygame`, `numpy`, `mediapipe`
* Try out demo implementations of CVGL with `tictactoe.py`, `snake.py`, `pong.py`, `spaceinvaders.py`, `spaceface.py`
* **Implementation in new games**: The jist of it is:
  - `import cvGameDevTools` *CVGL library
  - `import cv2` *openCV*
  - Instantiate `CvTool` object, passing in the window resolution of the game in question
  - Use `capture_frame()` from cvGameDevTools to capture game display as openCV compatible image
  - Use`frame_step()` from cvGameDevTools to return info such as hand, face and finger positions and gestures
  - Use info returned from `frame_step()` as you would any other keyboard or mouse input event.
  - A window with the camera video feed overlayed on the game screen will be automatically created

#### Game-specific demo instructions

**FOR BEST RESULTS, KEEP RAISED FINGERS ORIENTED UPWARD WITH RESPECT TO FRAME**

* **Tic-tac-Toe** 
  - Keep fists clenched to prevent accidental move
  - Raising only index finger, drag the pink circle to where you want to make a move.
  - With index finger raised, raise middle finger up. This triggers a move by the player. 
  - Clench fist and remove hand from frame, allowing other player to then make their move.
  - Clicking on board with mouse also works
  - 
* **Snake** 
  - Player 1: Use direction arrows on keyboard to move snake. Maroon squares = food; blue squares - traps.
  - Player 2: Use raised index fingers to spawn food; use raised index and middle fingers to spawn traps.

* **Pong** 
  - Use two fingers raised to move right paddle
  - Keyboard direction buttons also work

* **Space Invaders**
  - Use index finger raised to move spaceship
  - Use two fingers to start firing (for best experience, keep index finger raised and flick middle finger (as if flicking a booger) to fire)
  - Keyboard direction buttons and space bar also works

* **Space Face**
  - Yellow ship: WASD movement + left CTRL to fire
  - Red ship: Keyboard direction arrow movement + right CTRL to fire
  - Dimensional Horror: 
    - Place face in frame. This controls the position of the monster
    - Index finger controls position of the hand. Move hand to left or right of screen to change targets.
    - Raise both fingers to fire projectiles at ship. They home in on targets!

* **Space Face**
  -
## Credit

### pyGame, OpenCV, mediapipe tutorial resources and game assets
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
- Aretha Fontaine
