# %%
from htw_search.build_index_pickles import load_paragraph_embeddings_for_bi_encoder
from htw_search.search import compute_top_k_bi_encoder_results

# %%

paragraph_embeddings, paragraphs = load_paragraph_embeddings_for_bi_encoder()
print(paragraph_embeddings.shape)
print(len(paragraphs))

# %%
results = compute_top_k_bi_encoder_results(
    "computer science", paragraph_embeddings, paragraphs
)

# %%
print([result.text_on_page.abbreviated_text for result in results])
