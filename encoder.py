import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials 
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://facerecogattendencesys-default-rtdb.firebaseio.com/","storageBucket":"facerecogattendencesys.appspot.com"})

folderPath = 'images'
PathList = os.listdir(folderPath)
# print(PathList)
imgList = []
person_id = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    # print(path)
    # print(os.path.splitext(path)[0])
    person_id.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


# print(imgList)
# print(person_id)


def generateEncoding(imgList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        enc = face_recognition.face_encodings(img)[0]
        encodeList.append(enc)
    return encodeList

print("encoding Started....")
encodeListKnown = generateEncoding(imgList)
encodeListKnownWithIds = [encodeListKnown,person_id]
print("encoding Complete....")  

file = open("encodefile.p","wb")
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("File saved....")  