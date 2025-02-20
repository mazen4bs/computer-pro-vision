# computer-pro-vision
This app lets you control your computer entirely hands-free, without the need for a mouse, touchpad, or physical buttons, using only your computer's camera—offering functionality similar to Apple Vision Pro but tailored for desktops and laptops.
# Hand Gesture-Based Mouse & Scroll Control

This project implements a **hand gesture-based system** for controlling the mouse pointer, clicking, scrolling, and adjusting volume using a webcam. It utilizes **OpenCV, Mediapipe, and PyAutoGUI** to track hand landmarks and translate them into on-screen interactions.

## Features
✅ **Mouse Movement** - Move your hand to control the cursor with smooth tracking.  
✅ **Click & Double Click** - Pinch gestures trigger left-click and double-click actions.  
✅ **Scrolling** - Bring the middle finger close to the thumb and move up/down to scroll.  
✅ **Volume Control** - Adjust system volume using the distance between fingers.  
✅ Right Click - Open a context menu by forming a fist with the hand. <br>
Multi-Touch Zooming – Use two hands or fingers to zoom in and out on images or webpages.(not completed)



## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mazen4bs/computer-pro-vision.git
   cd computer-pro-vision
   ```
2. Run the program:
   ```bash
   python main.py
   ```

## Usage
- Move your **index finger** to control the cursor.
- **Thumb & Index Finger Pinch** → Click.
- **Thumb & Middle Finger Pinch** → Right Click.
- **Thumb & Index Finger** → Double Click.
- **Thumb & Middle Finger Pinch + Up/Down Motion** → Scroll up and down.
- **fingers up or down for Volume control**.

## Dependencies
- Python 3.7+
- OpenCV
- Mediapipe
- PyAutoGUI
- NumPy

Install missing dependencies with:
```bash
pip install opencv-python mediapipe pyautogui numpy
```

## File Structure
```
📂 gesture-mouse-control
 ├── 📜 main.py              # Main execution file
 ├── 📜 MouseControl.py      # Handles cursor movement, clicking, and scrolling
 ├── 📜 VolumeControl.py     # Adjusts system volume via hand gestures
 ├── 📜 HandTrackingModule.py # Hand tracking with Mediapipe
 ├── 📜 requirements.txt     # Required Python packages
 ├── 📜 README.md            # Documentation
```
