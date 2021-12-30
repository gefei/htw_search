# %%
from sentence_transformers import SentenceTransformer
from .env import load_config

# %%
_config = load_config()

bi_encoder_name = _config["bi_encoder_name"]
cross_encoder_name = _config["cross_encoder_name"]

bi_encoder = SentenceTransformer(bi_encoder_name)
cross_encoder = SentenceTransformer(cross_encoder_name)
