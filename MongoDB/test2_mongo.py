import pymongo, json
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client.mydb
collection = db.mycollection

with open("accounts.json", "r") as file:
    data = json.load(file)

result = collection.insert_many(data)

print("Inserted data with the following IDs:", result.inserted_ids)

index_name = "city_index"
collection.create_index("address.city", name=index_name)

city = "Bradshawborough"
results = collection.find({"address.city": city})

for result in results:
    print(result)

min_balance = 30000
results = collection.find({"balance": {"$gt": min_balance}})

for result in results:
    print(result)

pipeline = [
    {"$group": {"_id": "$address.city", "total_balance": {"$sum": "$balance"}}},
    {"$sort": {"total_balance": -1}}
]

results = collection.aggregate(pipeline)

for result in results:
    print(f"{result['_id']}: {result['total_balance']}")

collection.delete_many({"email": None}) # Pour éviter les emails vides
index_name = collection.create_index("email", unique=True)

pipeline = [
    {"$match": {"age": {"$gt": 25}}},
    {"$group": {"_id": "$age", "count": {"$sum": 1}}}
]

results = collection.aggregate(pipeline)

for result in results:
    print(result)