from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo import MongoClient
from routes import router
from constants import DATABASE_TEST, MONGO_CONNECTION_STRING

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(MONGO_CONNECTION_STRING)
    app.database = app.mongodb_client[DATABASE_TEST]

@app.on_event("shutdown")
async def shutdown_event():
    app.database.drop_collection("urls")
    app.mongodb_client.close()

app.include_router(router)

def test_create_shortcode_url_pair():
    with TestClient(app) as client:
        response = client.post("/shorten", json={"url":"https://www.amazon.com/", "shortcode" : "777777"})
        assert response.status_code == 201
        
        body = response.json()
        assert body.get("shortcode") == "777777"