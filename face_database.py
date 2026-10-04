import os
import cv2
import pickle

from face_detection import detect_faces
from face_recognation import get_face_feature


# --------------------------------
# Dataset and database paths
# --------------------------------

DATASET_PATH = "data/users"
DATABASE_PATH = "face_database.pkl"


# --------------------------------
# Create face database
# --------------------------------

def create_face_database():

    face_database = {}

    # Go through each person's folder
    for person_name in os.listdir(DATASET_PATH):

        person_path = os.path.join(DATASET_PATH, person_name)

        # Skip anything that is not a folder
        if not os.path.isdir(person_path):
            continue

        features = []

        # Go through every image of this person
        for image_name in os.listdir(person_path):

            image_path = os.path.join(person_path, image_name)

            image = cv2.imread(image_path)

            if image is None:
                print(f"Could not read: {image_path}")
                continue

            # Detect faces
            faces = detect_faces(image)

            if faces is None or len(faces) == 0:
                print(f"No face found: {image_path}")
                continue

            # Use the first detected face
            face = faces[0]

            # Generate face feature
            feature = get_face_feature(image, face)

            if feature is None:
                print(f"Could not create feature: {image_path}")
                continue

            features.append(feature)

        # Store this person's features
        if features:
            face_database[person_name] = features

            print(
                f"{person_name}: "
                f"{len(features)} face features created"
            )

        else:
            print(f"{person_name}: no valid face features")

    # Save database
    with open(DATABASE_PATH, "wb") as file:
        pickle.dump(face_database, file)

    print("\nFace database created successfully.")


# --------------------------------
# Run directly
# --------------------------------

if __name__ == "__main__":
    create_face_database()


  