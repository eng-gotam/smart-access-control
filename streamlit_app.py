import streamlit as st
import cv2
import numpy as np

from face_detection import detect_faces
from face_recognation import get_face_feature
from authorization import authorize_face
from logger import log_access


# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="Smart Access Control",
    page_icon="🔐",
    layout="centered"
)


# --------------------------------
# Title
# --------------------------------

st.title("🔐 Smart Access Control System")

st.write(
    "Face recognition-based access control using "
    "OpenCV YuNet and SFace."
)


# --------------------------------
# Camera input
# --------------------------------

image = st.camera_input("Take a picture")


# --------------------------------
# Process image
# --------------------------------

if image is not None:

    # Convert uploaded image to OpenCV format
    image_bytes = image.getvalue()

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    frame = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    # --------------------------------
    # Detect faces
    # --------------------------------

    faces = detect_faces(frame)

    if faces is None or len(faces) == 0:

        st.error("❌ No face detected.")

    else:

        all_authorized = True
        results = []

        # --------------------------------
        # Recognize every detected face
        # --------------------------------

        for face in faces:

            feature = get_face_feature(
                frame,
                face
            )

            result = authorize_face(feature)

            name = result["name"]
            score = result["score"]
            authorized = result["authorized"]

            results.append(
                {
                    "name": name,
                    "score": score,
                    "authorized": authorized
                }
            )

            # Draw bounding box
            x, y, w, h = face[:4].astype(int)

            if authorized:
                box_color = (0, 255, 0)
                label = f"{name} | AUTHORIZED | {score:.2f}"
            else:
                box_color = (0, 0, 255)
                label = f"UNKNOWN | UNAUTHORIZED | {score:.2f}"
                all_authorized = False

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                box_color,
                2
            )

            cv2.putText(
                frame,
                label,
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                box_color,
                2
            )

        # --------------------------------
        # Display processed image
        # --------------------------------

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        st.image(
            frame_rgb,
            caption="Processed Camera Image",
            use_container_width=True
        )

        # --------------------------------
        # Access decision
        # --------------------------------

        if all_authorized:

            st.success("🟢 ACCESS GRANTED")

            names = ", ".join(
                result["name"]
                for result in results
            )

            scores = [
                result["score"]
                for result in results
            ]

            average_score = sum(scores) / len(scores)

            st.write(
                f"**Authorized:** {names}"
            )

            st.write(
                f"**Average similarity:** {average_score:.2f}"
            )

            st.info("🚪 Gate would OPEN.")

            log_access(
                names,
                "AUTHORIZED",
                average_score
            )

        else:

            st.error("🔴 ACCESS DENIED")

            names = ", ".join(
                result["name"]
                for result in results
                if result["authorized"]
            )

            if names:
                st.write(
                    f"Authorized person detected: {names}"
                )

            st.warning(
                "At least one detected person is unauthorized."
            )

            st.info("🚪 Gate would remain CLOSED.")

            scores = [
                result["score"]
                for result in results
            ]

            average_score = sum(scores) / len(scores)

            log_access(
                "Unknown",
                "UNAUTHORIZED",
                average_score
            )