"""
training.py — Train the LBPH Face Recognizer
=============================================
Scans all images in the TrainingImage/ folder, detects faces using Haar Cascade,
and trains an LBPH model saved to TrainingImageLabel/trainer.yml

Usage:
    python training.py
"""

import cv2
import os
import numpy as np
from PIL import Image

BASE_DIR          = os.path.dirname(os.path.abspath(__file__))
TRAINING_IMAGE_DIR = os.path.join(BASE_DIR, "TrainingImage")
TRAINING_LABEL_DIR = os.path.join(BASE_DIR, "TrainingImageLabel")
HAARCASCADE_PATH  = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
TRAINER_PATH      = os.path.join(TRAINING_LABEL_DIR, "trainer.yml")

os.makedirs(TRAINING_LABEL_DIR, exist_ok=True)

# Initialize recognizer and detector
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector   = cv2.CascadeClassifier(HAARCASCADE_PATH)


def get_images_and_labels(path: str):
    """
    Load face images and their corresponding enrollment IDs from disk.

    Args:
        path: Directory containing training images.
              Expected filename format: Name.EnrollmentID.Count.jpg

    Returns:
        face_samples: List of grayscale face image arrays.
        ids:          List of integer enrollment IDs.
    """
    image_paths = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    face_samples = []
    ids = []

    for img_path in image_paths:
        try:
            # Open image in grayscale
            pil_img = Image.open(img_path).convert("L")
            img_arr = np.array(pil_img, dtype=np.uint8)

            # Parse enrollment ID from filename: Name.EnrollmentID.Count.jpg
            filename = os.path.basename(img_path)
            parts    = filename.split(".")
            if len(parts) < 3:
                print(f"[SKIP] Unexpected filename format: {filename}")
                continue
            enrollment_id = int(parts[1])

            # Detect faces in the image
            detected_faces = detector.detectMultiScale(img_arr)
            for (x, y, w, h) in detected_faces:
                face_samples.append(img_arr[y : y + h, x : x + w])
                ids.append(enrollment_id)

        except Exception as e:
            print(f"[WARN] Could not process {img_path}: {e}")

    return face_samples, ids


def train():
    """Train LBPH recognizer and save the model."""
    print(f"[INFO] Loading training images from: {TRAINING_IMAGE_DIR}")
    faces, ids = get_images_and_labels(TRAINING_IMAGE_DIR)

    if not faces:
        print("[ERROR] No face samples found. Capture images first (run AMS_Run.py).")
        return

    print(f"[INFO] Training on {len(faces)} face samples...")
    recognizer.train(faces, np.array(ids))
    recognizer.write(TRAINER_PATH)
    print(f"[SUCCESS] Model trained and saved to: {TRAINER_PATH}")
    print(f"          Unique students: {len(set(ids))}")


if __name__ == "__main__":
    train()
