from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from helpers import isValidShortCode, generateRandomShortCode

class UrlItemBody(BaseModel):
    url: str
    shortcode: str | None = None

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/shorten", status_code=201)
async def create_shorturl(urlbody: UrlItemBody, request: Request):
    if urlbody.url is None:
        raise HTTPException(status_code=400, detail="Url not present")
    
    if (urlbody.shortcode is None or urlbody.shortcode == ""):
        generatedShordCode = generateRandomShortCode()
        collisionClearance = False
        while(not collisionClearance):
            check_for_collision = request.app.database["urls"].find_one({"shortcode": urlbody.shortcode})
            if not check_for_collision:
                collisionClearance = True
            else:
                generatedShordCode = generateRandomShortCode()

        urlItemEncoded = jsonable_encoder({"url": urlbody.url, "shortcode" : generatedShordCode})
        new_urlItem = request.app.database["urls"].insert_one(urlItemEncoded)
        created_urlItem = request.app.database["urls"].find_one({"_id": new_urlItem.inserted_id})
        
        return {"shortcode" : generatedShordCode}
    
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

@router.get("/{shortcode}", status_code=302)
def read_root(shortcode, request: Request):
    foundShortcode = request.app.database["urls"].find_one({"shortcode": shortcode})
    if(foundShortcode):
        return {"url": foundShortcode['url']}
    else:
        raise HTTPException(status_code=404, detail="Shortcode not found")

@router.get("/{shortcode}/stats", status_code=200)
def read_root(shortcode):
    return {"stats": shortcode}