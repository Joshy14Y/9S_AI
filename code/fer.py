import cv2

def recognizeFaces(image):
    img = cv2.imread(image)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_classifier.detectMultiScale(
        gray_img, scaleFactor=1.1, minNeighbors=17, minSize=(40, 40)
    )

    resized_faces = []
    for (x, y, w, h) in faces:
        face_img = gray_img[y:y+h, x:x+w]
        resized_face = cv2.resize(face_img, (40, 40))
        resized_faces.append(resized_face)

    return resized_faces

if __name__ == "__main__":
    image_path = "C:/Users/Joshua/Desktop/AI_Project_P1/tst/group.jpg"
    detected_faces = recognizeFaces(image_path)
    print("Number of faces detected:", len(detected_faces))

    for i, face in enumerate(detected_faces):
        cv2.imshow(f"Resized Face {i+1}", face)
        cv2.waitKey(0)
        cv2.destroyAllWindows()