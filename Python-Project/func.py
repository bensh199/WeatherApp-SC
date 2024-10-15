from flask import Flask, request, jsonify
from pymongo import MongoClient
from kafka import KafkaConsumer
import os

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = f'mongodb://admin:admin@{os.getenv("MONGODB_HOST")}/'
DB_NAME = 'purchases'
COLLECTION_NAME = 'items'

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Kafka configuration
KAFKA_SERVERS = f'{os.getenv("KAFKA_HOST")}'
KAFKA_TOPIC = 'purchased-items'

# Connect to Kafka
consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_SERVERS, group_id='my_consumer_group')

# Function to consume Kafka messages and add purchases to MongoDB
def consume_and_add_purchases():
    for message in consumer:
        print(message)
        data = message.value.decode('utf-8').strip('"').split(',')
        print(data)
        bought_amount = data[0]
        item_name = data[1]
        user_id = data[2]
        user_pass = data[3]
        add_purchase(user_id, item_name, bought_amount, user_pass)

# Function to add a purchase to MongoDB
def add_purchase(user_id, item_name, bought_amount, user_pass):
    print("#######################################")
    print(bought_amount)
    print("#######################################")
    print("#######################################")
    print(item_name)
    print("#######################################")
    print("#######################################")
    print(user_id)
    print("#######################################")
    purchase = {
        'user_id': user_id,
        'item_id': item_name,
        'bought_amount': bought_amount,
        'user_pass': user_pass
    }
    collection.insert_one(purchase)

def get_purchased_items(credentials):
    print(credentials)
    print(credentials[0], credentials[1])
    query = {
    '$and': [
        {'user_id': f'{credentials[0]}'},
        {'user_pass': f'{credentials[1]}'},
        ]
    }
    projection = {
    '_id': False,  # Exclude the _id field
    'item_id': True,  # Include the item_id field
    'bought_amount': True,  # Include the bought_amount field
}
    purchased_items = list(collection.find(query, projection))
    print(purchased_items)
    return purchased_items

if __name__ == '__main__':
    # Start Kafka consumer thread
    # kafka_consumer_thread = Thread(target=consume_and_add_purchases)
    # kafka_consumer_thread.daemon = True
    # kafka_consumer_thread.start()

    # # Run Flask app
    # app.run(debug=True)

    pass