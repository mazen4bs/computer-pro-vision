import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) 
ctime = 0
ptime = 0
mpHands = mp.solutions.hands # Hands module 
hands = mpHands.Hands() # Hands object
mpDraw = mp.solutions.drawing_utils # Drawing module
while True: 
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert to RGB as hands class only use rgb
    results = hands.process(imgRGB) # Process the image
    #print(results.multi_hand_landmarks) # Print the landmarks
    if results.multi_hand_landmarks: # If there are hands
        for handLms in results.multi_hand_landmarks: # For each hand
            for id, lm in enumerate(handLms.landmark): # For each landmark
                h, w, c = img.shape # Get the height, width and channels
                cx, cy = int(lm.x*w), int(lm.y*h) # Get the x and y coordinates
                if id in (8, 4): 
                    print(id, cx, cy) 
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)       
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) 

    ctime = time.time()
    fps = 1/(ctime-ptime)    
    ptime = ctime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3) # Display the FPS

    cv2.imshow("Image", img)
    cv2.waitKey(1) 