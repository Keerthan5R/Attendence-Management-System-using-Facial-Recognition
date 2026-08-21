"""
testing.py — Live Face Recognition Test
========================================
A lightweight standalone script to test the trained model against the webcam.
Draws bounding boxes with predicted student IDs and confidence scores.

Usage:
    python testing.py
    Press Q to quit.
"""

import cv2
import os
import numpy as np

BASE_DIR          = os.path.dirname(os.path.abspath(__file__))
HAARCASCADE_PATH  = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
TRAINER_PATH      = os.path.join(BASE_DIR, "TrainingImageLabel", "trainer.yml")

# --- Load the trained model ---------------------------------------------------
if not os.path.exists(TRAINER_PATH):
    raise FileNotFoundError(
        f"Trained model not found at: {TRAINER_PATH}\n"
        "Please run training.py first."
    )

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(TRAINER_PATH)

face_cascade = cv2.CascadeClassifier(HAARCASCADE_PATH)
font = cv2.FONT_HERSHEY_SIMPLEX

# --- Start webcam feed --------------------------------------------------------
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    raise RuntimeError("Could not access webcam. Check your camera connection.")

print("[INFO] Starting face recognition test. Press Q to quit.")

while True:
    ret, frame = cam.read()
    if not ret:
        print("[WARN] Failed to read from webcam.")
        break

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in faces:
        student_id, confidence = recognizer.predict(gray[y : y + h, x : x + w])

        if confidence < 70:
            label = f"ID: {student_id}"
            color = (0, 255, 0)   # Green — recognized
        else:
            label = "Unknown"
            color = (0, 0, 255)   # Red — unknown

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label,             (x, y - 10), font, 0.8, color, 2)
        cv2.putText(frame, f"Conf: {confidence:.1f}", (x, y + h + 20), font, 0.6, (255, 255, 0), 1)

    cv2.putText(frame, "Press Q to quit", (10, 30), font, 0.7, (255, 255, 255), 2)
    cv2.imshow("Face Recognition Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
print("[INFO] Test session ended.")
