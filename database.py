
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://facerecogattendencesys-default-rtdb.firebaseio.com/"})

ref = db.reference('students')

data ={
    "231":
    {
            "name": "Elon Musk",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
    },
    "232":
    {
            "name": "Lakshya verma",
            "major": "Programming",
            "starting_year": 2022,
            "total_attendance": 8,
            "standing": "A",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
    }
}

# sending data to database
for key,value in data.items():
    ref.child(key).set(value)