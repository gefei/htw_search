from pydantic import BaseModel
from fastapi import FastAPI

class Query(BaseModel):
    query: str

class SearchResult(BaseModel):
    url: str


app = FastAPI()

@app.post("/search/")
def create_item(query: Query):
    return SearchResult(url="http://localhost")

