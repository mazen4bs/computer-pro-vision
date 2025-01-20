import pyautogui
import numpy as np
import time

class VolumeControl:
    def __init__(self, angle_threshold=0.1, idle_time=0.5):
        self.prev_index_finger = None  # To store the previous position of the index finger
        self.prev_thumb_base = None  # To store the previous position of the thumb base
        self.prev_angle = None  # To store the previous calculated angle
        self.prev_direction = None  # To store the previous direction
        self.last_movement_time = time.time()  # Time of last movement
        self.angle_threshold = angle_threshold  # Minimum angle change to trigger volume change
        self.idle_time = idle_time  # Idle time threshold to reset volume control

    def control_volume(self, index_finger, thumb_base):
        if self.prev_index_finger is None or self.prev_thumb_base is None:
            self.prev_index_finger = index_finger
            self.prev_thumb_base = thumb_base
            return None  # No previous position to compare

        # Calculate angle change
        angle = self.calculate_angle(index_finger, thumb_base)

        if self.prev_angle is not None:
            angle_change = angle - self.prev_angle  # Difference in angle

            # Only consider significant angle changes to avoid unnecessary actions
            if abs(angle_change) > self.angle_threshold:  # Threshold to prevent small movements from being considered
                if angle_change > 0:
                    self.prev_direction = "Clockwise"
                    print("Volume Up")
                    pyautogui.press('volumeup')  # Increase volume
                elif angle_change < 0:
                    self.prev_direction = "Counterclockwise"
                    print("Volume Down")
                    pyautogui.press('volumedown')  # Decrease volume

                self.last_movement_time = time.time()  # Reset idle time after movement
        elif time.time() - self.last_movement_time > self.idle_time:  # If idle for too long, stop detecting
            self.prev_angle = None  # Reset angle if idle for too long
            self.prev_index_finger = None  # Reset finger position
        
        self.prev_angle = angle
        self.prev_index_finger = index_finger  # Update previous position
        self.prev_thumb_base = thumb_base  # Update thumb base position

    def calculate_angle(self, current, previous):
        dx = current[0] - previous[0]
        dy = current[1] - previous[1]
        return np.arctan2(dy, dx)  # Calculate angle of movement
