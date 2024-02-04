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
        response = client.post("/shorten", json={"url":"https://www.amazon.com", "shortcode" : "777777"})
        assert response.status_code == 201
        
        body = response.json()
        assert body.get("shortcode") == "777777"

def test_url_missing():
    with TestClient(app) as client:
        response = client.post("/shorten", json={"url":"", "shortcode" : "777777"})
        assert response.status_code == 400
        
def test_shortcode_already_in_use():
    with TestClient(app) as client:
        client.post("/shorten", json={"url":"https://www.amazon.com", "shortcode" : "777777"})
        response = client.post("/shorten", json={"url":"https://www.amazon.com", "shortcode" : "777777"})
        assert response.status_code == 409

def test_invalid_shortcode():
    with TestClient(app) as client:
        response = client.post("/shorten", json={"url":"https://www.amazon.com", "shortcode" : "55!"})
        assert response.status_code == 412

def test_successful_shortcode_retreival():
    with TestClient(app) as client:
        client.post("/shorten", json={"url":"https://www.amazon.com", "shortcode" : "888888"})
        response = client.get("/888888")
        assert response.status_code == 302

def test__shortcode_notfound():
    with TestClient(app) as client:
        client.post("/shorten", json={"url":"https://www.amazon.com", "shortcode" : "888888"})
        response = client.get("/000000")
        assert response.status_code == 404

def test__shortcode_stats_redirect_count():
    with TestClient(app) as client:
        client.post("/shorten", json={"url":"https://www.amazon.com", "shortcode" : "888888"})
        client.get("/888888")
        client.get("/888888")
        response = client.get("/888888/stats")
        body = response.json()

        assert response.status_code == 200
        assert body.get("redirectCount") == 2

def test__shortcode_stats_notfound():
    with TestClient(app) as client:
        client.post("/shorten", json={"url":"https://www.amazon.com", "shortcode" : "888888"})
        response = client.get("/000000/stats")
        assert response.status_code == 404