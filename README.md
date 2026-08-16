# Touchless Mouse Using Computer Vision

This project is a simple touchless mouse system that allows the user to control the mouse using hand gestures in front of a webcam.

The webcam captures the hand, and MediaPipe is used to detect the hand landmarks. Based on the position and angle of the fingers, different mouse actions are performed.

## What it can do

* Move the mouse using the index finger
* Left click
* Right click
* Double click
* Scroll
* Take a screenshot

I also added cursor smoothing so that the cursor does not move too much because of small hand movements. A click cooldown was added to avoid the same click being triggered repeatedly.

## Technologies Used

Python was used for the main implementation.

The project uses:

* OpenCV for accessing the webcam
* MediaPipe for hand tracking
* PyAutoGUI for cursor movement, scrolling and screenshots
* Pynput for mouse clicks

## How to Run

Clone the repository:

```bash
git clone https://github.com/faizunnisa105/Touchless-Mouse-Using-Computer-Vision.git
```

Go into the project folder:

```bash
cd Touchless-Mouse-Using-Computer-Vision
cd live_mouse_control_using_hand_gestures
```

Install the required libraries:

```bash
pip install opencv-python mediapipe pyautogui pynput
```

Run the program:

```bash
python main.py
```

A webcam window will open and the hand landmarks will be displayed.

Press `Q` to close the application.

## How the Gestures Work

The program uses the 21 hand landmarks provided by MediaPipe. It checks the position of the fingers and calculates distances and angles between selected landmarks.

The index finger is mainly used for cursor movement. Different combinations of the index and middle fingers are used for clicking, double clicking and scrolling.

## Project Structure

```text
Touchless-Mouse-Using-Computer-Vision
│
├── live_mouse_control_using_hand_gestures
│   ├── main.py
│   └── util.py
│
└── README.md
```

## Improvements I Made

The project was originally based on an existing hand gesture mouse implementation. I studied the code and modified it for my own version.

The changes I worked on include:

* Smoother cursor movement
* Click cooldown
* Gesture-based scrolling
* Improved status messages while performing actions

## Future Improvements

I would like to improve the project further by adding better gesture detection, adjustable cursor sensitivity, drag and drop gestures and more customizable controls.

## Author

Faizunnisa

GitHub: https://github.com/faizunnisa105
ok