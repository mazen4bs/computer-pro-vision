import cv2
import time
from VolumeControl import VolumeControl  
from HandTrackingModule import HandTracker
from MouseControl import MouseControl  

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # Set width to 1280 pixels
    cap.set(4, 720)   # Set height to 720 pixels

    pTime = 0
    detector = HandTracker()
    volume_control = VolumeControl(detector, threshold_up=145, threshold_down=145)
    mouse_control = MouseControl(screen_width=1920, screen_height=1080, smoothing=7)

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if lmList:
            index_finger_pos = lmList[8][1], lmList[8][2]  # Index finger tip
            thumb_tip = lmList[4][1], lmList[4][2]  # Thumb tip
            middle_tip = lmList[12][1], lmList[12][2]  # Middle finger tip

            mouse_control.move_pointer(index_finger_pos, thumb_tip)
            mouse_control.click(thumb_tip, index_finger_pos)
            mouse_control.right_click(thumb_tip, middle_tip) 
            mouse_control.scroll(thumb_tip, middle_tip)  

        # Volume Control
        volume_control.control_volume(img)

        # Calculate and Display FPS
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

