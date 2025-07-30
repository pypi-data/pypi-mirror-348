""""Model definitions"""


# from models.use_multilingual_models import use_multilingual_v3_model
from lingtrain_aligner.sentence_transformers_models import (
    sentence_transformers_model,
    sentence_transformers_model_labse,
    sentence_transformers_model_xlm_100,
    rubert_tiny,
    sonar,
)

models = {
    "sentence_transformer_multilingual": sentence_transformers_model,
    "sentence_transformer_multilingual_xlm_100": sentence_transformers_model_xlm_100,
    "sentence_transformer_multilingual_labse": sentence_transformers_model_labse,
    "rubert_tiny": rubert_tiny,
    "sonar": sonar,
    # "use_multilingual_v3": use_multilingual_v3_model
}
