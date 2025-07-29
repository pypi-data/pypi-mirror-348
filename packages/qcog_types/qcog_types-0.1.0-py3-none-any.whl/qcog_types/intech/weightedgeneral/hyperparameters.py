from pydantic import BaseModel


class Hyperparameters(BaseModel):
    """Hyperparameters for the Weighted General model."""
    epochs: int
    hilbert_space_dims: int
    learning_rate: float
    weighted_learning_rate: float
    target: str
    batch_size: int
    seed: int
