import cv2
import time
from VolumeControl import VolumeControl  # Import the VolumeControl class
from HandTrackingModule import HandTracker  # Import the HandTracker class

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = HandTracker()
    volume_control = VolumeControl(detector)  # Pass the hand tracker instance to VolumeControl

    while True:
        success, img = cap.read()
        img = detector.findHands(img)  # Detect hands

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
