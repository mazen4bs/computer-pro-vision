import cv2
import time
from VolumeControl import VolumeControl  # Import the VolumeControl class
from HandTrackingModule import HandTracker  # Import the HandTracker class
from MouseControl import MouseControl  # Import the MouseControl class

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # Set width to 1280 pixels
    cap.set(4, 720)   # Set height to 720 pixels

    pTime = 0
    detector = HandTracker()
    volume_control = VolumeControl(detector, threshold_up=145, threshold_down=145)  # Customize thresholds
    mouse_control = MouseControl(screen_width=1920, screen_height=1080, smoothing=7)  # Initialize MouseControl

    while True:
        success, img = cap.read()
        img = detector.findHands(img)  # Detect hands
        lmList = detector.findPosition(img)  # Get landmark positions

        if lmList:
            # Handle mouse pointer movement
            index_finger_pos = lmList[8][1], lmList[8][2]  # Index finger tip
            mouse_control.move_pointer(index_finger_pos, lmList[4][1:3])  # Move pointer

            # Handle mouse click
            thumb_tip = lmList[4][1], lmList[4][2]  # Thumb tip
            index_tip = lmList[8][1], lmList[8][2]  # Index finger tip
            mouse_control.click(thumb_tip, index_tip, threshold=30)

        # Let VolumeControl handle volume adjustment
        volume_control.control_volume(img)

        # Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
