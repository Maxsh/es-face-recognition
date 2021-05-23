import face_recognition
import numpy as np
import sys
image = face_recognition.load_image_file(sys.argv[1])
# detect the faces from the images
face_locations = face_recognition.face_locations(image)
# encode the 128-dimension face encoding for each face in the image
face_encodings = face_recognition.face_encodings(image, face_locations)
# Display the 128-dimension for each face detected
for face_encoding in face_encodings:
      print("Face found ==>  ", face_encoding.tolist())