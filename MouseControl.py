import pyautogui
import numpy as np

class MouseControl:
    def __init__(self, screen_width=1920, screen_height=1080, smoothing=5, padding=1, scaling_factor=4, scroll_threshold=50,click_threshold=30):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.smoothing = smoothing
        self.prev_location = None  # Store the previous location for smoothing
        self.padding = padding  # Padding to prevent reaching edges
        self.scaling_factor = scaling_factor  # Amplify small hand movements
        self.scroll_threshold = scroll_threshold  # Threshold for activating scrolling
        self.scroll_active = False  # Track if scrolling is happening
        self.prev_scroll_y = None  # Track previous Y position for smooth scrolling
        self.click_threshold = click_threshold  # Threshold for clicks


    def move_pointer(self, index_pos, thumb_pos):
      x = (index_pos[0] + thumb_pos[0]) / 2  
      y = (index_pos[1] + thumb_pos[1]) / 2  

      # Invert Left-Right Movement (Moving right moves cursor left, and vice versa)
      screen_x = np.interp(x, [0, 1280], [self.screen_width - self.padding, self.padding])  
      screen_y = np.interp(y, [0, 720], [self.padding, self.screen_height - self.padding])

      # Apply Smoothing for smoother motion
      if self.prev_location is None:
          self.prev_location = (screen_x, screen_y)
      else:
          prev_x, prev_y = self.prev_location
          screen_x = prev_x + (screen_x - prev_x) / self.smoothing
          screen_y = prev_y + (screen_y - prev_y) / self.smoothing
          self.prev_location = (screen_x, screen_y)

      pyautogui.moveTo(screen_x, screen_y)


    def click(self, thumb_tip, index_tip, threshold=30):
        """Triggers a mouse click if thumb and index finger are close."""
        dx = thumb_tip[0] - index_tip[0]
        dy = thumb_tip[1] - index_tip[1]
        distance = np.sqrt(dx**2 + dy**2)

        if distance < threshold:
            pyautogui.click()

    def right_click(self, thumb_tip, middle_tip):
          dx = thumb_tip[0] - middle_tip[0]
          dy = thumb_tip[1] - middle_tip[1]
          distance = np.sqrt(dx**2 + dy**2)

          if distance < self.click_threshold:
              pyautogui.rightClick()

    def scroll(self, thumb_tip, middle_tip):
        """Scrolls when the middle finger and thumb are close, based on vertical movement."""

        # Calculate distance between middle finger tip and thumb tip
        dx = thumb_tip[0] - middle_tip[0]
        dy = thumb_tip[1] - middle_tip[1]
        distance = np.sqrt(dx**2 + dy**2)

        if distance < self.scroll_threshold:
            if not self.scroll_active:
                # First time fingers come close, store initial Y position
                self.start_scroll_y = middle_tip[1]
                self.scroll_active = True
                return  # Avoid sudden jump at start

            # Calculate relative movement from the starting point
            scroll_amount = (middle_tip[1] - self.start_scroll_y) // 5  # Adjust sensitivity

            if scroll_amount > 0:
                pyautogui.scroll(int(abs(scroll_amount) * 2))  # Scroll UP (inverted)
            elif scroll_amount < 0:
                pyautogui.scroll(-int(abs(scroll_amount) * 2))  # Scroll DOWN (inverted)

        else:
            # Reset when fingers separate
            self.scroll_active = False
            self.start_scroll_y = None
