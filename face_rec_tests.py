import cv2
import face_recognition
import numpy as np

ethan = face_recognition.load_image_file('./images/ethan.jpeg')
ethan_encoding = face_recognition.face_encodings(ethan)[0]

# zurgin = face_recognition.load_image_file('./images/zurgin.png')
# zurgin_encoding = face_recognition.face_encodings(zurgin)[0]

known_face_encodings = [ethan_encoding]
known_face_names = ['ethan']

while True:
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        rval, frame = vc.read()
        key = cv2.waitKey(20)

        small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "default"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_idx = np.argmax(face_distances)
            if matches[best_match_idx]:
                name = known_face_names[best_match_idx]
            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow("preview")