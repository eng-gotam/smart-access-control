import cv2

from face_detection import detect_faces
from face_recognation import get_face_feature
from authorization import authorize_face


# --------------------------------
# Start webcam
# --------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open camera.")
    exit()


print("Camera started.")
print("Press Q to quit.")


while True:

    success, frame = camera.read()

    if not success:
        print("Failed to read frame.")
        break

    # --------------------------------
    # Detect faces
    # --------------------------------

    faces = detect_faces(frame)

    if faces is not None:

        for face in faces:

            # --------------------------------
            # Extract face feature
            # --------------------------------

            feature = get_face_feature(
                frame,
                face
            )

            # --------------------------------
            # Authorize face
            # --------------------------------

            result = authorize_face(feature)

            name = result["name"]
            score = result["score"]
            authorized = result["authorized"]

            # --------------------------------
            # Display result
            # --------------------------------

            x, y, w, h = face[:4].astype(int)

            if authorized:

                label = f"{name} | AUTHORIZED | {score:.2f}"

            else:

                label = f"UNKNOWN | UNAUTHORIZED | {score:.2f}"

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # --------------------------------
    # Show camera
    # --------------------------------

    cv2.imshow(
        "Authorization Test",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()