import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, mode=False, maxHands=2, detectionConfidence=0.5, trackingConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfidence = float(detectionConfidence)
        self.trackingConfidence = float(trackingConfidence)

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionConfidence,
            min_tracking_confidence=self.trackingConfidence
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        """
        Detect hands in the image and optionally draw landmarks.

        :param img: Input image for hand detection
        :param draw: Whether to draw landmarks or not
        :return: The image with landmarks drawn (if `draw` is True)
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        """
        Get the position of hand landmarks.

        :param img: Input image
        :param handNo: The hand number to get positions for (use 0 for the first detected hand)
        :param draw: Whether to draw circles on landmarks or not
        :return: List of landmark positions [(id, x, y), ...]
        """
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))

                # Optionally draw specific points like index (8) and thumb (4)
                if draw and id in [8, 4]:  # Index finger (8) and Thumb (4)
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    
        return lmList

    def getHandCount(self):
        """Return the number of hands detected"""
        if self.results.multi_hand_landmarks:
            return len(self.results.multi_hand_landmarks)
        return 0

    def getClosestHand(self, img):
        """Get the closest hand to the camera (based on y-coordinate)"""
        lmList = self.findPosition(img)
        if not lmList:
            return None
        hands_y_coords = [lm[2] for lm in lmList]  # List of y-coordinates of the landmarks
        closest_hand_index = hands_y_coords.index(min(hands_y_coords))
        return closest_hand_index
