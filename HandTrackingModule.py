import cv2
import mediapipe as mp
import time

# Define the HandTracker class
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
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True): # handNo=0 means just on hand
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))
                if draw:
                    if id in (8, 4):
                      cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return lmList

# Define the main function at the end of the file
def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = HandTracker()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)  # Detect hands
        lmList = detector.findPosition(img)  # Get landmark positions

        if len(lmList) != 0:  # If landmarks detected
            print(lmList[4])  # Example: Print position of index finger tip
            print(lmList[8])
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

# Ensure the script starts executing from the main function
if __name__ == "__main__":
    main()
