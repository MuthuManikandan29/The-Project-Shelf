✍️ Air Drawing & Gesture Recognition with OpenCV and CVZone
This project allows users to draw in the air using hand gestures detected by their webcam. It utilizes MediaPipe-based hand tracking through the cvzone.HandTrackingModule and recognizes specific finger configurations to perform actions like drawing, pausing, clearing the canvas, or triggering predictions.

🎯 Features
🖐️ Real-time hand tracking using cvzone.HandDetector

✏️ Draw in the air with your index finger

⏸️ Pause/resume drawing using 2-finger gesture

🧼 Clear the canvas with a thumbs-up gesture

🤖 Placeholder for AI recognition trigger with 4-finger gesture

📸 Webcam input with canvas overlay


| Fingers Up        | Action                               |
| ----------------- | ------------------------------------ |
| `[0, 1, 0, 0, 0]` | Draw (Index finger only)             |
| `[0, 1, 1, 0, 0]` | Pause Drawing                        |
| `[0, 1, 1, 1, 1]` | Trigger AI Recognition (placeholder) |
| `[1, 0, 0, 0, 0]` | Clear Canvas                         |


Press q to quit the program.

📌 Notes
Stable gesture recognition is handled using a deque buffer to avoid flickering due to minor finger movement.

Canvas and webcam image are blended for a smooth UX.

AI recognition functionality is a placeholder — you can plug in a trained model where indicated in the code.

🧠 Future Improvements
Integrate gesture classification using a trained CNN model.

Add gesture-based menu selection.

Save canvas as image.

Multi-hand support.