

import os
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import pymongo
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl
import random

load_dotenv()

DB_URL = os.getenv('DB_URL')
DB_NAME = os.getenv('DB_NAME')

client = pymongo.MongoClient(DB_URL)
db = client[DB_NAME]

app = FastAPI(title='Url Shortner',
              description="This api endpoint helps your shorten long urls.",
              version="1.0.0"
              )

@app.get('/')
def home():
    return "Welcome to rolo. Go to /docs to see API documentation."

@app.get('/api/', response_model=HttpUrl)
def shorten(url : HttpUrl):
    id_ = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(4))
    if db.urls.find_one({'url':url})!=None:
        id_ = db.urls.find_one({'url':url})['id']
        url_ = 'https://maphor.herokuapp.com/p/'+id_
        return url_
    else:
        db.urls.insert_one({'id':id_,'url':url})
        url_ = 'https://maphor.herokuapp.com/p/'+id_
        return url_

@app.get('/p/{id_}')
def route(id_:str):
    url = db.urls.find_one({'id':id_})['url']
    return RedirectResponse(url,status_code=302)
        