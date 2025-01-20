import pyautogui
import numpy as np

class MouseControl:
    def __init__(self, screen_width=1920, screen_height=1080, smoothing=3, padding=10):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.smoothing = smoothing
        self.prev_location = None  # Store the previous location for smoothing
        self.padding = padding  # Padding to prevent reaching edges

    def move_pointer(self, thumb_pos, index_pos):
        # Calculate the midpoint between thumb and index finger
        x = (thumb_pos[0] + index_pos[0]) / 2
        y = (thumb_pos[1] + index_pos[1]) / 2

        # Map the midpoint to the screen size with padding
        screen_x = np.interp(x, [0, 640], [self.padding, self.screen_width - self.padding])
        screen_y = np.interp(y, [0, 480], [self.padding, self.screen_height - self.padding])
        screen_y = self.screen_height - screen_y  # Invert y-axis for natural movement

        # Apply smoothing
        if self.prev_location is None:
            self.prev_location = (screen_x, screen_y)
        else:
            prev_x, prev_y = self.prev_location
            screen_x = prev_x + (screen_x - prev_x) / self.smoothing
            screen_y = prev_y + (screen_y - prev_y) / self.smoothing
            self.prev_location = (screen_x, screen_y)

        # Move the pointer
        pyautogui.moveTo(screen_x, screen_y)

    def click(self, thumb_tip, index_tip, threshold=30):
        # Calculate distance between thumb and index finger
        dx = thumb_tip[0] - index_tip[0]
        dy = thumb_tip[1] - index_tip[1]
        distance = np.sqrt(dx**2 + dy**2)

        # Perform a click if the fingers are close enough
        if distance < threshold:
            pyautogui.click()
