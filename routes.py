from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from helpers import isValidShortCode, generateRandomShortCode, getFormatedDateTimeStringNow, validateUrlFormat

class UrlItemBody(BaseModel):
    url: str
    shortcode: str | None = None

router = APIRouter()

@router.get("/")
def say_hello():
    return {"Hello": "World"}


@router.post("/shorten", status_code=201)
async def create_shorturl(urlbody: UrlItemBody, request: Request):

    #Validates url to be present
    if (urlbody.url is None or urlbody.url == ""):
        raise HTTPException(status_code=400, detail="Url not present")
    
    #Validates url to be of the right format (otherwise this endpoint becomes a string shortener)
    if (not validateUrlFormat(urlbody.url)):
        raise HTTPException(status_code=400, detail="Invalid url")
    
    #Generates and assigns random shortcode in case one is not present in the request
    #Checks for possible collisions
    #Stores the url/shortcode pair in the db
    if (urlbody.shortcode is None or urlbody.shortcode == ""):
        generatedShordCode = generateRandomShortCode()
        collisionClearance = False
        while(not collisionClearance):
            check_for_collision = request.app.database["urls"].find_one({"shortcode": urlbody.shortcode})
            if not check_for_collision:
                collisionClearance = True
            else:
                generatedShordCode = generateRandomShortCode()

        urlItemEncoded = jsonable_encoder({"url": urlbody.url, 
                                           "shortcode" : generatedShordCode,
                                            "created": getFormatedDateTimeStringNow(), 
                                            "lastRedirect": "", 
                                            "redirectCount": 0})
        new_urlItem = request.app.database["urls"].insert_one(urlItemEncoded)
        created_urlItem = request.app.database["urls"].find_one({"_id": new_urlItem.inserted_id})
        
        return {"shortcode" : generatedShordCode}
    
    #Validates the provided shortcode format before moving on
    if (not isValidShortCode(urlbody.shortcode)):
        raise HTTPException(status_code=412, detail="The provided shortcode is invalid")
    
    #Checks the provided shortcode does not already exist in the database
    check_existing_shortcode = request.app.database["urls"].find_one(
        {"shortcode": urlbody.shortcode}
    )
    if check_existing_shortcode:
        raise HTTPException(status_code=409, detail="Shortcode already in use")
    
    #Stores the provided shortcode/url pair in the db
    urlItemEncoded = jsonable_encoder({"url": urlbody.url, 
                                       "shortcode" : urlbody.shortcode, 
                                       "created": getFormatedDateTimeStringNow(), 
                                       "lastRedirect": "", "redirectCount": 0})
    new_urlItem = request.app.database["urls"].insert_one(urlItemEncoded)
    created_urlItem = request.app.database["urls"].find_one(
        {"_id": new_urlItem.inserted_id}
    )

    return {"shortcode" : created_urlItem['shortcode']}

@router.get("/{shortcode}", status_code=302)
def go_to_url(shortcode, request: Request):
    foundShortcode = request.app.database["urls"].find_one({"shortcode": shortcode})
    if(foundShortcode):
        request.app.database["urls"].update_one(
            {"shortcode": foundShortcode["shortcode"]}, 
            {"$set": {"lastRedirect": getFormatedDateTimeStringNow(), "redirectCount": foundShortcode["redirectCount"] + 1 }}
        )
        raise HTTPException(status_code=302, headers={"Location": foundShortcode['url']})
    else:
        raise HTTPException(status_code=404, detail="Shortcode not found")

@router.get("/{shortcode}/stats", status_code=200)
def get_shortcode_stats(shortcode, request: Request):
    foundShortcode = request.app.database["urls"].find_one({"shortcode": shortcode})
    if(foundShortcode):
        return {"created": foundShortcode["created"], 
                "lastRedirect": foundShortcode["lastRedirect"], 
                "redirectCount": foundShortcode["redirectCount"]}
    else:
        raise HTTPException(status_code=404, detail="Shortcode not found")