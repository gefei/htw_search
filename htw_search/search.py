from dataclasses import dataclass

from sentence_transformers import util

from .page import TextOnPage
from .utils.transformers import bi_encoder


NO_SCORE = -100.0


@dataclass
class ScoredText:
    text_on_page: TextOnPage
    bi_score: float = NO_SCORE
    cross_score: float = NO_SCORE


# The `filter_duplicates` parameter is a hack to work around the fact that we will be
# indexing both paragraphs and sentences, and therefore we duplicate results for
# single-sentence paragraphs. It would be more efficient to filter the duplicates
# when generating the embeddings, but then we could not easily compare results when
# using only one of the embeddings.
#
def compute_top_k_bi_encoder_results(
    query: str, corpus_embeddings, corpus_data, top_k=10, filter_duplicates=False
) -> list[ScoredText]:
    question_embedding = bi_encoder.encode(query, convert_to_tensor=True)
    question_embedding = question_embedding.cpu()  # or cuda()

    search_top_k = 2 * top_k if filter_duplicates else top_k
    raw_hits: list[dict] = compute_bi_encoder_hits(
        question_embedding, corpus_embeddings, search_top_k
    )
    candidate_results: list[ScoredText] = compute_bi_encoder_candidate_results(
        raw_hits, corpus_data
    )

    if filter_duplicates:
        results = remove_duplicates(candidate_results, top_k)
    else:
        results = candidate_results

    return results


def compute_bi_encoder_hits(
    question_embedding, corpus_embeddings, top_k: int
) -> list[dict]:
    raw_hits = util.semantic_search(
        question_embedding, corpus_embeddings=corpus_embeddings, top_k=top_k
    )
    # We only have a single query
    raw_hits = raw_hits[0]
    return raw_hits


def compute_bi_encoder_candidate_results(
    raw_hits: list[dict], corpus_data: list
) -> list[ScoredText]:
    return [
        ScoredText(text_on_page=corpus_data[hit["corpus_id"]], bi_score=hit["score"])
        for hit in raw_hits
    ]


# noinspection PyShadowingNames
def remove_duplicates(
    candidate_results: list[ScoredText], top_k: int, use_enclosing_paragraphs=False
) -> list[ScoredText]:
    results = []
    last_text, last_page = "", None
    get_text = (
        lambda a: a.paragraph_text if use_enclosing_paragraphs else lambda a: a.text
    )
    for result in candidate_results:
        top = result.text_on_page
        text = get_text(top)
        if text == last_text and top.page == last_page:
            continue
        last_text, last_page = text, top.page
        results.append(result)
        if len(results) == top_k:
            break
    return results
