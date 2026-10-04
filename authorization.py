import pickle
import base64
import os

from face_recognation import compare_faces

DATABASE_PATH = "face_database.pkl"
COSINE_THRESHOLD = 0.60


def load_face_database():

    # 1. Try local database first
    if os.path.exists(DATABASE_PATH):
        try:
            with open(DATABASE_PATH, "rb") as file:
                return pickle.load(file)
        except Exception as e:
            print(f"Error loading local face database: {e}")

    # 2. Try Streamlit Secrets
    try:
        import streamlit as st

        if "FACE_DATABASE" in st.secrets:

            encoded_database = st.secrets["FACE_DATABASE"]

            database_bytes = base64.b64decode(
                encoded_database
            )

            face_database = pickle.loads(
                database_bytes
            )

            return face_database

    except Exception as e:
        print(f"Error loading face database from secrets: {e}")

    print("Face database not found.")

    return {}


def find_best_match(face_feature, face_database):

    best_name = "Unknown"
    best_score = -1.0

    for person_name, stored_features in face_database.items():

        for stored_feature in stored_features:

            score = compare_faces(
                face_feature,
                stored_feature
            )

            if score > best_score:
                best_score = score
                best_name = person_name

    return best_name, best_score


def authorize_face(face_feature):

    face_database = load_face_database()

    if not face_database:

        return {
            "authorized": False,
            "name": "Unknown",
            "score": 0.0
        }

    best_name, best_score = find_best_match(
        face_feature,
        face_database
    )

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


if __name__ == "__main__":

    database = load_face_database()

    if database:

        print("Face database loaded successfully.")

        print("\nRegistered users:")

        for person_name, features in database.items():

            print(
                f"- {person_name}: {len(features)} features"
            )

    else:

        print("Face database is empty.")