import pickle
import cv2

from face_recognation import compare_faces


# --------------------------------
# Face database path
# --------------------------------

DATABASE_PATH = "face_database.pkl"


# --------------------------------
# Authorization threshold
# --------------------------------

COSINE_THRESHOLD = 0.60


# --------------------------------
# Load face database
# --------------------------------

def load_face_database():

    try:

        with open(DATABASE_PATH, "rb") as file:
            face_database = pickle.load(file)

        return face_database

    except FileNotFoundError:

        print("Face database not found.")
        return {}


# --------------------------------
# Find best matching person
# --------------------------------

def find_best_match(face_feature, face_database):

    best_name = "Unknown"
    best_score = -1.0

    # Go through every person
    for person_name, stored_features in face_database.items():

        # Compare with every feature of that person
        for stored_feature in stored_features:

            score = compare_faces(
                face_feature,
                stored_feature
            )

            if score > best_score:

                best_score = score
                best_name = person_name

    return best_name, best_score


# --------------------------------
# Authorize face
# --------------------------------

def authorize_face(face_feature):

    # Load database
    face_database = load_face_database()

    if not face_database:

        return {
            "authorized": False,
            "name": "Unknown",
            "score": 0.0
        }

    # Find best match
    best_name, best_score = find_best_match(
        face_feature,
        face_database
    )

    # Check threshold
    if best_score >= COSINE_THRESHOLD:

        return {
            "authorized": True,
            "name": best_name,
            "score": best_score
        }

    else:

        return {
            "authorized": False,
            "name": "Unknown",
            "score": best_score
        }


# --------------------------------
# Simple test
# --------------------------------

if __name__ == "__main__":

    database = load_face_database()

    if database:

        print("Face database loaded successfully.")

        print("\nRegistered users:")

        for person_name, features in database.items():

            print(
                f"- {person_name}: "
                f"{len(features)} features"
            )

    else:

        print("Face database is empty.")