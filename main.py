import os
import pickle

import cv2
import cvzone
import face_recognition
import firebase_admin
import numpy as np
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://facerecogattendencesys-default-rtdb.firebaseio.com/",
                              "storageBucket": "facerecogattendencesys.appspot.com"})

cap = cv2.VideoCapture(0)
# 0 ---> web cam,  1---> phone cam
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

folderModePath = 'Resources/Modes'
modesPathList = os.listdir(folderModePath)
imgModeList = []

for path in modesPathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

"""load the Encoding File"""

print("loading encoded file....")
file = open("encodefile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, person_id = encodeListKnownWithIds
print("encoded file loded....")

modeType = 0
counter = 0

while (True):
    ret, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]
    cv2.imshow("Face attendence", imgBackground)
    # cv2.imshow("Face attendence", img)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        facedis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # lower the distance , better the match
        # print("matches",matches)
        # print("facedis", facedis)
        matchIndex = np.argmin(facedis)
        # print("matchIndex",matchIndex)
        if matches[matchIndex]:
            # print("known face detected")
            # print("Person Id",person_id[matchIndex])

            """--------------------Creating rectangle start---------------"""
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            """--------------------Creating rectangle end    ---------------"""
            id = person_id[matchIndex]
            # print(id)
            if counter == 0:
                counter = 1
                modeType = 1
    if counter != 0:

        if counter == 1:
            personsinfo = db.reference(f'students/{id}').get()
            print(personsinfo)

        cv2.putText(imgBackground, str(personsinfo['total_attendance']), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (55, 100, 255), 1)
        
        (w,h)=cv2.getTextSize(personsinfo['name'], cv2.FONT_HERSHEY_COMPLEX,1,1)
        # offset = (414-w)//2
        # cv2.putText(imgBackground, str(personsinfo['name']), (808+offset, 445),
        #             cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

        cv2.putText(imgBackground, str(personsinfo['major']), (1020, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (55, 100, 255), 1)

        cv2.putText(imgBackground, str(id), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (55, 100, 255), 1)

        cv2.putText(imgBackground, str(personsinfo['standing']), (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (55, 100, 255), 1)

        cv2.putText(imgBackground, str(personsinfo['year']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (55, 100, 255), 1)

        cv2.putText(imgBackground, str(personsinfo['starting_year']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (55, 100, 255), 1)

        counter += 1

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
