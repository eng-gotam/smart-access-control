import cv2
from face_detection import detect_faces


# Load test image
image = cv2.imread("data/users/gotam/gotam1.jpg")

if image is None:
    print("Image could not be loaded.")
    exit()


# Detect faces
faces = detect_faces(image)

print("Faces detected:", faces)


# Draw detected faces
if faces is not None:

    for face in faces:

        x, y, w, h = face[:4].astype(int)

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )


# Display image
cv2.imshow("Face Detection Test", image)

cv2.waitKey(0)
cv2.destroyAllWindows()