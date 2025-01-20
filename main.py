# main.py
import cv2
import mediapipe as mp
import time
from VolumeControl import VolumeControl  # Import the VolumeControl class
from HandTrackingModule import HandTracker  # Import the HandTracker class

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = HandTracker()
    volume_control = VolumeControl(angle_threshold=0.92)  # Only angle-based control

    while True:
        success, img = cap.read()
        img = detector.findHands(img)  # Detect hands
        lmList = detector.findPosition(img)  # Get landmark positions

        if len(lmList) != 0:  # If landmarks detected
            index_finger = lmList[8][1], lmList[8][2]  # Get the index finger tip (x, y)
            thumb_base = lmList[4][1], lmList[4][2]  # Get the base of the thumb (x, y)
            volume_control.control_volume(index_finger, thumb_base)  # Pass positions to VolumeControl

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
