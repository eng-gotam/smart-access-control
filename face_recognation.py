import cv2
import numpy as np


# --------------------------------
# Load face recognition model
# --------------------------------

face_recognizer = cv2.FaceRecognizerSF.create(
    "models/face_recognition_sface_2021dec.onnx",
    ""
)


# --------------------------------
# Extract face feature
# --------------------------------

def get_face_feature(frame, face):

    # Align and crop the detected face
    aligned_face = face_recognizer.alignCrop(frame, face)

    # Extract the face feature / embedding
    feature = face_recognizer.feature(aligned_face)

    return feature


# --------------------------------
# Compare two face features
# --------------------------------

def compare_faces(feature1, feature2):

    similarity = face_recognizer.match(
        feature1,
        feature2,
        cv2.FaceRecognizerSF_FR_COSINE
    )

    return similarity

