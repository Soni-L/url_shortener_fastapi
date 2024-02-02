from pymongo import MongoClient
from fastapi import FastAPI
from routes import router

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    # The connection string here is dangerously exposed in the code for simplicity sake, it should never be done this way in a real prod env
    app.mongodb_client = MongoClient("mongodb+srv://typetone:Hjw9iRm74cY4qpBS@cluster0.7dxtavv.mongodb.net/")
    app.database = app.mongodb_client["test"]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(router)
