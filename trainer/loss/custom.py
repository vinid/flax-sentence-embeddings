import jax
from jax import numpy as jnp
from .basic import padded_cross_entropy_loss
from ..utils.ops import cos_sim


@jax.jit
def multiple_negatives_ranking_loss(embeddings: jnp.DeviceArray, scale: float = 20.0,
                                    similarity_fct=cos_sim):

    embeddings_a = embeddings[:, 0, :]
    # positive and hard negatives (if any, flattened and treated as additional samples).
    embeddings_b = jnp.reshape(embeddings[:, 1:, :], (-1, embeddings.shape[-1]))

    scores = similarity_fct(embeddings_a, embeddings_b) * scale
    assert scores.shape == (len(embeddings_b), len(embeddings_a))

    labels = jnp.arange(len(embeddings_a), dtype=jnp.uint64)
    return padded_cross_entropy_loss(scores, labels)
