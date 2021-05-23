import face_recognition
import numpy as np
import sys
import json

file = sys.argv[1]
name = sys.argv[2]

image = face_recognition.load_image_file(file)
# detect the faces from the images
face_locations = face_recognition.face_locations(image)
# encode the 128-dimension face encoding for each face in the image
face_encodings = face_recognition.face_encodings(image, face_locations)

file = open("var/face.json", "w")
face = {
    "face_name": name,
    "face_encoding": []
}
for face_encoding in face_encodings:
     face["face_encoding"] = face_encoding.tolist()
     file.write(json.dumps(face))
     print(json.dumps(face))

file.close()