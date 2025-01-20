import pyautogui

class VolumeControl:
    def __init__(self, hand_tracker, threshold_up=100, threshold_down=100):
        self.hand_tracker = hand_tracker  # Use the HandTracker instance
        self.threshold_up = threshold_up  # Threshold for fingers to be considered "up"
        self.threshold_down = threshold_down  # Threshold for fingers to be considered "down"

    def control_volume(self, img):
        lmList = self.hand_tracker.findPosition(img)  # Get landmark positions

        if len(lmList) != 0:  # If landmarks detected
            # Check positions of index and middle fingers
            index_tip = lmList[8][2]  # y-coordinate of index finger tip
            index_base = lmList[5][2]  # y-coordinate of index finger base
            middle_tip = lmList[12][2]  # y-coordinate of middle finger tip
            middle_base = lmList[9][2]  # y-coordinate of middle finger base

            # Check if the fingers are "up" or "down" with separate thresholds
            index_up = index_tip < index_base - self.threshold_up
            middle_up = middle_tip < middle_base - self.threshold_up
            index_down = index_tip > index_base + self.threshold_down
            middle_down = middle_tip > middle_base + self.threshold_down

            # Adjust volume based on finger states
            if index_up and middle_up:
                self.volume_up()
            elif index_down and middle_down:
                self.volume_down()

    def volume_up(self):
        print("Volume Up")
        pyautogui.press('volumeup')  # Increase volume

    def volume_down(self):
        print("Volume Down")
        pyautogui.press('volumedown')  # Decrease volume
