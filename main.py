import requests
import redis
import json
from fastapi import FastAPI

rd = redis.Redis(host="localhost", port=6379, db=0, password='redispasswd')

app = FastAPI()


@app.get("/")
def read_root():
    return "Hello World"


@app.get("/users/{id}")
def read_user(id: int):

    cache = rd.get(id)
    if cache:
        print("Cache hit.")
        return json.loads(cache)
    else:
        print("Cache miss.")
        r = requests.get(
            f"https://jsonplaceholder.typicode.com/users/{id}")
        rd.set(id, r.text)
        # expire in 5s
        rd.expire(id, 5)
        return r.json()
