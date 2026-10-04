import cv2


# --------------------------------
# Load face detection model
# --------------------------------

face_detector = cv2.FaceDetectorYN.create(
    "models/face_detection_yunet_2023mar.onnx",
    "",
    (640, 640),
    0.5,    # score threshold
    0.3,    # NMS threshold
    5000    # top_k
)


# --------------------------------
# Detect faces
# --------------------------------

def detect_faces(frame):

    # Get frame height and width
    height, width = frame.shape[:2]

    # Update detector input size
    face_detector.setInputSize((width, height))

    # Detect faces
    _, faces = face_detector.detect(frame)

    return faces


# --------------------------------
# Test with webcam
# --------------------------------

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)

    while True:

        success, frame = camera.read()

        if not success:
            print("Failed to read frame from camera.")
            break

        faces = detect_faces(frame)

        if faces is not None:

            for face in faces:

                x, y, w, h = face[:4].astype(int)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

        cv2.imshow("Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()



