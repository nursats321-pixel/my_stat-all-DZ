from pymongo import MongoClient
import redis


# MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["catalog_db"]
products_collection = mongo_db["products"]


# Redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)