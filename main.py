import random
import string
import requests
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from db.database import engine, get_db, Base
from db.models import UrlModel

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return RedirectResponse(url="http://localhost:8000/docs")


def generate_code(input):
    code = random.choices(input, k=6)
    code = "".join(code)
    return code


@app.post("/shorten", status_code=201)
async def short_url(url: HttpUrl = Body(..., embed=True, example="https://www.example.com"),
                    shortcode: Optional[str] = None,
                    db: Session = Depends(get_db)):
    obj = UrlModel()
    VALID_SC_INPUT = string.ascii_letters + string.digits + '_'
    shortcode_len = 6

    request = requests.get(url)
    if request.status_code != 200:
        raise HTTPException(status_code=400, detail="URL not present")

    url_link = db.query(UrlModel).filter_by(original_url=url).first()
    if url_link:
        raise HTTPException(status_code=409, detail="URL already present")

    obj.original_url = url

    # If shortcode provided, check valid format and existence in db
    if shortcode is not None:
        # First check valid format of the shortcode
        if len(shortcode) > shortcode_len or len(shortcode) < shortcode_len:
            raise HTTPException(status_code=412,
                                detail="The provided shortcode is invalid (Length of shortcode should be 6")

        for c in shortcode:
            if c not in VALID_SC_INPUT:
                raise HTTPException(status_code=412,
                                    detail="The provided shortcode is invalid "
                                           "(Shortcode must contain alphanumeric characters or underscore)")

        # Check if shortcode exists in db
        url_sc = db.query(UrlModel).filter_by(shortcode=shortcode).first()

        if url_sc:
            raise HTTPException(status_code=409, detail="Shortcode already in use")

        obj.shortcode = shortcode
    else:
        # Generate shortcode
        while True:
            rand_code = generate_code(VALID_SC_INPUT)
            rand_code_exists = db.query(UrlModel).filter_by(shortcode=rand_code).first()
            if not rand_code_exists:
                obj.shortcode = rand_code
                # response.status_code = status.HTTP_201_CREATED
                break

    db.add(obj)
    db.commit()

    return {
        "original_url": obj.original_url,
        "shortcode": obj.shortcode
    }


@app.get("/{shortcode}", status_code=status.HTTP_302_FOUND)
def redirect(shortcode: str = None, db: Session = Depends(get_db)):
    url_sc = db.query(UrlModel).filter_by(shortcode=shortcode).first()

    if url_sc is None:
        raise HTTPException(status_code=404, detail="Shortcode not found")

    url_sc.redirectCount = url_sc.redirectCount + 1
    url_sc.lastRedirect = datetime.now(timezone.utc)

    db.add(url_sc)
    db.commit()

    redirect_url = url_sc.original_url

    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    return response._headers


@app.get("/{shortcode}/stats")
def shortcode_stats(shortcode: str = None, db: Session = Depends(get_db)):
    url_sc = db.query(UrlModel).filter_by(shortcode=shortcode).first()

    if url_sc is None:
        raise HTTPException(status_code=404, detail="Shortcode not found")
    else:
        created = db.query(UrlModel).filter_by(shortcode=shortcode).first().created
        lastRedirect = db.query(UrlModel).filter_by(shortcode=shortcode).first().lastRedirect
        redirectCount = db.query(UrlModel).filter_by(shortcode=shortcode).first().redirectCount

    return {
        "created": created,
        "lastRedirect": lastRedirect,
        "redirectCount": redirectCount
    }
