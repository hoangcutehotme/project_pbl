from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['detection_pbl']
collection = db['detections']

