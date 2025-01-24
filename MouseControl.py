import pyautogui
import numpy as np
import time

class MouseControl:
    def __init__(self, screen_width=1920, screen_height=1080, smoothing=5, padding=1, scaling_factor=4):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.smoothing = smoothing
        self.prev_location = None  # Store the previous location for smoothing
        self.padding = padding  # Padding to prevent reaching edges
        self.scaling_factor = scaling_factor  # Amplify small hand movements
        self.last_click_time = 0  # Track the time of the last click
        self.double_click_threshold = 0.3  # Time threshold for detecting double-click (300 ms)

    def move_pointer(self, thumb_pos, index_pos):
        # Calculate the midpoint between thumb and index finger
        x = (thumb_pos[0] + index_pos[0]) / 2
        y = (thumb_pos[1] + index_pos[1]) / 2

        # Map the midpoint to the screen size with scaling and padding
        screen_x = np.interp(x, [0, 1280], 
                             [self.screen_width - self.padding, self.padding])
        screen_y = np.interp(y, [0, 720], 
                             [self.padding, self.screen_height - self.padding])

        # Amplify cursor movement by scaling factor
        if self.prev_location is None:
            self.prev_location = (screen_x, screen_y)
        else:
            prev_x, prev_y = self.prev_location
            delta_x = (screen_x - prev_x) * self.scaling_factor
            delta_y = (screen_y - prev_y) * self.scaling_factor
            screen_x = prev_x + delta_x / self.smoothing
            screen_y = prev_y + delta_y / self.smoothing
            self.prev_location = (screen_x, screen_y)

        # Move the pointer
        pyautogui.moveTo(screen_x, screen_y)

    def click(self, thumb_tip, index_tip, threshold=30):
        # Calculate distance between thumb and index finger
        dx = thumb_tip[0] - index_tip[0]
        dy = thumb_tip[1] - index_tip[1]
        distance = np.sqrt(dx**2 + dy**2)

        # Perform a single or double click if fingers are close enough
        if distance < threshold:
            current_time = time.time()
            time_since_last_click = current_time - self.last_click_time

            if time_since_last_click <= self.double_click_threshold:
                pyautogui.doubleClick()  # Perform a double-click
                print("Double Click")
            else:
                pyautogui.click()  # Perform a single click
                print("Single Click")

            self.last_click_time = current_time  # Update the last click time
