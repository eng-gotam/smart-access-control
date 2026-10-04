import cv2
import time

from face_detection import detect_faces
from face_recognation import get_face_feature
from authorization import authorize_face
from gate_controller import control_gate, is_gate_open
from logger import log_access


# --------------------------------
# Settings
# --------------------------------

AUTHORIZED_FRAMES = 5
UNAUTHORIZED_FRAMES = 3
NO_FACE_FRAMES = 10

GATE_OPEN_SECONDS = 5
COOLDOWN_SECONDS = 30


# --------------------------------
# Counters
# --------------------------------

authorized_count = 0
unauthorized_count = 0
no_face_count = 0


# --------------------------------
# Timers
# --------------------------------

gate_open_time = None
cooldown_start_time = None


# --------------------------------
# Access states
# --------------------------------

WAITING = "WAITING"
OPEN = "OPEN"
WAITING_FOR_EXIT = "WAITING_FOR_EXIT"
COOLDOWN = "COOLDOWN"

state = WAITING


# --------------------------------
# Start camera
# --------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open camera.")
    exit()

print("Smart Access Control started.")
print("Press Q to quit.")


# --------------------------------
# Main loop
# --------------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("Failed to read frame.")
        break


    # --------------------------------
    # Detect faces
    # --------------------------------

    faces = detect_faces(frame)


    # --------------------------------
    # Default values
    # --------------------------------

    all_authorized = False

    detected_names = []
    detected_scores = []


    # --------------------------------
    # No face
    # --------------------------------

    if faces is None or len(faces) == 0:

        no_face_count += 1

        authorized_count = 0
        unauthorized_count = 0


    # --------------------------------
    # Faces detected
    # --------------------------------

    else:

        no_face_count = 0

        all_authorized = True


        # --------------------------------
        # Recognize every face
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


            detected_names.append(name)
            detected_scores.append(score)


            x, y, w, h = face[:4].astype(int)


            # --------------------------------
            # Person status
            # --------------------------------

            if authorized:

                label = (
                    f"{name} | "
                    f"AUTHORIZED | "
                    f"{score:.2f}"
                )

            else:

                label = (
                    "UNKNOWN | "
                    "UNAUTHORIZED | "
                    f"{score:.2f}"
                )

                all_authorized = False


            # --------------------------------
            # Draw face box
            # --------------------------------

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
        # Stability counters
        # --------------------------------

        if all_authorized:

            authorized_count += 1
            unauthorized_count = 0

        else:

            unauthorized_count += 1
            authorized_count = 0


    # ==================================================
    # STATE 1: WAITING
    # ==================================================

    if state == WAITING:


        if authorized_count >= AUTHORIZED_FRAMES:

            control_gate(True)

            gate_open_time = time.time()

            state = OPEN


            # --------------------------------
            # Log authorized access
            # --------------------------------

            names = ", ".join(detected_names)

            if detected_scores:

                average_score = (
                    sum(detected_scores)
                    / len(detected_scores)
                )

            else:

                average_score = 0.0


            log_access(
                names,
                "AUTHORIZED",
                average_score
            )


            authorized_count = 0
            unauthorized_count = 0


    # ==================================================
    # STATE 2: OPEN
    # ==================================================

    elif state == OPEN:


        elapsed_time = (
            time.time()
            - gate_open_time
        )


        if elapsed_time >= GATE_OPEN_SECONDS:

            control_gate(False)

            gate_open_time = None

            state = WAITING_FOR_EXIT

            print(
                "Gate timeout reached."
            )


    # ==================================================
    # STATE 3: WAITING FOR EXIT
    # ==================================================

    elif state == WAITING_FOR_EXIT:


        if no_face_count >= NO_FACE_FRAMES:

            cooldown_start_time = time.time()

            state = COOLDOWN

            no_face_count = 0
            authorized_count = 0
            unauthorized_count = 0

            print(
                "Person left. "
                "Starting cooldown."
            )


    # ==================================================
    # STATE 4: COOLDOWN
    # ==================================================

    elif state == COOLDOWN:


        elapsed_cooldown = (
            time.time()
            - cooldown_start_time
        )


        if elapsed_cooldown >= COOLDOWN_SECONDS:

            cooldown_start_time = None

            state = WAITING

            print(
                "Cooldown finished. "
                "System ready."
            )


    # --------------------------------
    # Display state
    # --------------------------------

    if state == OPEN:

        remaining = (
            GATE_OPEN_SECONDS
            - (time.time() - gate_open_time)
        )

        if remaining < 0:
            remaining = 0

        status = (
            f"GATE: OPEN "
            f"({remaining:.1f}s)"
        )


    elif state == WAITING_FOR_EXIT:

        status = "WAITING FOR EXIT"


    elif state == COOLDOWN:

        remaining = (
            COOLDOWN_SECONDS
            - (time.time() - cooldown_start_time)
        )

        if remaining < 0:
            remaining = 0

        status = (
            f"COOLDOWN "
            f"({remaining:.1f}s)"
        )


    elif unauthorized_count > 0:

        status = "CHECKING ACCESS"


    else:

        status = "GATE: CLOSED"


    # --------------------------------
    # Display status
    # --------------------------------

    cv2.putText(
        frame,
        status,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )


    # --------------------------------
    # Display camera
    # --------------------------------

    cv2.imshow(
        "Smart Access Control",
        frame
    )


    # --------------------------------
    # Quit
    # --------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# --------------------------------
# Safety shutdown
# --------------------------------

control_gate(False)

camera.release()
cv2.destroyAllWindows()

print(
    "Smart Access Control stopped."
)