import face_recognition
import numpy as np
from elasticsearch import Elasticsearch
import sys
import json

image = face_recognition.load_image_file(sys.argv[1])
# detect the faces from the images
face_locations = face_recognition.face_locations(image)
# encode the 128-dimension face encoding for each face in the image
face_encodings = face_recognition.face_encodings(image, face_locations)

# Connect to Elasticsearch cluster
from elasticsearch import Elasticsearch
es = Elasticsearch(
    host="es",
    port=9200,
)

i = 0
for face_encoding in face_encodings:
    print("Location", json.dumps(face_locations[i]))
    print("Face", i+1)
    response = es.search(
        index="faces",
        body={
            "size": 1,
            "_source": "face_name",
            "query": {
                "script_score": {
                     "query" : {
                         "match_all": {}
                     },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'face_encoding')",
                        "params": {
                            "query_vector":face_encoding.tolist()
                        }
                    }
                }
            }
        }
    )
    for hit in response['hits']['hits']:
        if (float(hit['_score']) > 0.9):
            print("==> This face match with",hit['_source']['face_name'],"; the score is" ,hit['_score'])
        else:
            print("==> Unknown face")
    i += 1
