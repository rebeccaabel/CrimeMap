from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

URI = 'mongodb+srv://rebeccaabel:StGzyB9rUeSaVF9i@cluster0.tgvserh.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(URI, server_api=ServerApi('1'))
db = client["CrimeMap"]
collection = db["crime_data"]

collection.create_index("Date", unique=True)

try: 
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/api/markers')
def get_markers():
    try: 
        markers = list(collection.find({}, {"_id": 0}))
        return jsonify(markers)
    except Exception as e: 
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)