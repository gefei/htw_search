from htw_search.build_index_pickles import load_paragraph_embeddings_for_bi_encoder
from htw_search.page import TextOnPage
from htw_search.search import compute_top_k_bi_encoder_results

from pydantic import BaseModel
from fastapi import FastAPI


paragraph_embeddings, paragraphs = load_paragraph_embeddings_for_bi_encoder()

class Query(BaseModel):
    query: str

class SearchResult(BaseModel):
    url: str


app = FastAPI()

@app.post("/search/")
def create_item(query: Query):
    results: list[TextOnPage] = compute_top_k_bi_encoder_results(
        query.query, paragraph_embeddings, paragraphs, filter_duplicates=True
    )
    return [SearchResult(url=result.text_on_page.page.url) for result in results]

@app.get("/")
def index():
    return "hello world"
