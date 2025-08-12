import asyncio
from functools import wraps

from pymongo import AsyncMongoClient

CLIENT = AsyncMongoClient()


beltbot_db = CLIENT.beltbot_db
REQUESTS = beltbot_db.REQUESTS
STATS = beltbot_db.STATS

requests_collection = REQUESTS
stats_collection = STATS

COLLECTIONS = {"REQUESTS": requests_collection, "STATS": stats_collection}


# generic


async def _insert(collection, document):
    await collection.insert_one(document)


async def _find(collection, field, value):
    return await collection.find_one({field: value})


async def _find_all(collection):
    cursor = collection.find({})
    return [document for document in await cursor.to_list(length=100)]


async def _delete(collection, field, value):
    await collection.delete_many({field: value})


async def _delete_all(collection):
    await collection.delete_many({})


async def _update(collection, field, value, replacement, remove=False):
    await collection.update_one(
        {field: value}, {"$set" if not remove else "$unset": replacement}
    )


async def _update_increment(collection, field, increment):
    await collection.update_one({"_id": field}, {"$inc": {"count": increment}})


# belt_stuff


async def add_request(belt_request):
    await _insert(requests_collection, belt_request)


async def get_request(request_id):
    return await _find(requests_collection, "_id", request_id)


async def update_request(request_id, obj, remove=False):
    await _update(requests_collection, "_id", request_id, obj, remove)


async def delete_request(request_id):
    await _delete(requests_collection, "_id", request_id)


async def delete_all_requests():
    await _delete_all(requests_collection)


async def get_all_requests():
    return await _find_all(requests_collection)


# stats


async def update_stats(key, increment=1):
    await _update_increment(stats_collection, key, increment)


async def get_stats():
    return await _find_all(stats_collection)
