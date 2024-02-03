from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from helpers import isValidShortCode

class UrlItemBody(BaseModel):
    url: str
    shortcode: str | None = None

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/shorten")
async def create_shorturl(urlbody: UrlItemBody, request: Request):
    if urlbody.url is None:
        raise HTTPException(status_code=400, detail="Url not present")
    
    if (urlbody.shortcode is None or urlbody.shortcode == ""):
        return {"shortcode" : 777}
    
    check_existing_shortcode = request.app.database["urls"].find_one(
        {"shortcode": urlbody.shortcode}
    )
    if check_existing_shortcode:
        raise HTTPException(status_code=409, detail="Shortcode already in use")
    
    if (not isValidShortCode(urlbody.shortcode)):
        raise HTTPException(status_code=412, detail="The provided shortcode is invalid")
    

    urlItemEncoded = jsonable_encoder(urlbody)
    new_urlItem = request.app.database["urls"].insert_one(urlItemEncoded)
    created_urlItem = request.app.database["urls"].find_one(
        {"_id": new_urlItem.inserted_id}
    )

    return {"shortcode" : created_urlItem['shortcode']}