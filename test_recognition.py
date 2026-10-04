import cv2

from face_detection import detect_faces
from face_recognation import get_face_feature


image = cv2.imread("data/users/gotam/gotam1.jpg")

if image is None:
    print("Image could not be loaded.")
    exit()


faces = detect_faces(image)

if faces is None:
    print("No face detected.")
    exit()


print("Faces detected:", len(faces))


for i, face in enumerate(faces):

    x, y, w, h = face[:4].astype(int)

    print(f"Face {i + 1}: x={x}, y={y}, w={w}, h={h}")

    cv2.rectangle(
        image,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        2
    )

    cv2.putText(
        image,
        f"Face {i + 1}",
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )


cv2.imshow("Recognition Test", image)

cv2.waitKey(0)
cv2.destroyAllWindows()