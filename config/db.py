from pymongo import MongoClient
conn = MongoClient('mongodb://localhost:27017/')
db = conn['detection_pbl']
collection = db['detections']

