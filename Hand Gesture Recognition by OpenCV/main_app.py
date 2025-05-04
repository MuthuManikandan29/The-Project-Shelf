import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from collections import deque
from math import hypot
import time

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand detector
detector = HandDetector(detectionCon=0.85, maxHands=2)

# Canvas for drawing
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

prev_x, prev_y = 0, 0
draw = False

gesture_buffer = deque(maxlen=6)
gesture_name = ""

def get_stable_gesture(fingers):
    gesture_buffer.append(tuple(fingers))
    if len(gesture_buffer) == gesture_buffer.maxlen:
        most_common = max(set(gesture_buffer), key=gesture_buffer.count)
        if gesture_buffer.count(most_common) >= 5:
            return list(most_common)
    return None

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror view
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)

        stable_fingers = get_stable_gesture(fingers)
        if stable_fingers:
            x, y = lmList[8][0], lmList[8][1]  # Index finger tip

            # Gesture detection with smoothing
            if stable_fingers == [0, 1, 0, 0, 0]:
                gesture_name = "Drawing"
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x, y
                cv2.line(canvas, (prev_x, prev_y), (x, y), (255, 0, 255), 10)
                prev_x, prev_y = x, y

            elif stable_fingers == [0, 1, 1, 0, 0]:
                gesture_name = "Paused"
                prev_x, prev_y = 0, 0

            elif stable_fingers == [0, 1, 1, 1, 1]:
                gesture_name = "AI Recognition Triggered"
                # Prepare canvas for AI model
                sketch_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
                sketch_gray = cv2.resize(sketch_gray, (28, 28))
                sketch_gray = sketch_gray / 255.0
                sketch_input = sketch_gray.reshape(1, 28, 28, 1)

                # Uncomment below to use trained model
                # prediction = model.predict(sketch_input)
                # predicted_label = class_names[np.argmax(prediction)]

                # For now, just display the trigger
                cv2.putText(img, "Predicting...", (900, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                time.sleep(1)  # Delay for realism

            elif stable_fingers == [1, 0, 0, 0, 0]:
                gesture_name = "Canvas Cleared"
                canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
                prev_x, prev_y = 0, 0

            else:
                gesture_name = "No Action"
                prev_x, prev_y = 0, 0

        # Display hand type correctly (fix flipped labels)
        true_hand_type = "Right" if hand["type"] == "Left" else "Left"
        cv2.putText(img, f"Hand: {true_hand_type}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    # Merge canvas with webcam
    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, canvas)

    # Display gesture name
    cv2.putText(img, f"Gesture: {gesture_name}", (50, 180),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3)

    cv2.imshow("Air Drawing", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

