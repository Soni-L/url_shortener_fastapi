from pymongo import MongoClient
from fastapi import FastAPI
from routes import router
from constants import DATABASE_MAIN, MONGO_CONNECTION_STRING

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    # The connection string here is dangerously exposed in the code for simplicity sake, it should never be done this way in a real prod env
    app.mongodb_client = MongoClient(MONGO_CONNECTION_STRING)
    app.database = app.mongodb_client[DATABASE_MAIN]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(router)
