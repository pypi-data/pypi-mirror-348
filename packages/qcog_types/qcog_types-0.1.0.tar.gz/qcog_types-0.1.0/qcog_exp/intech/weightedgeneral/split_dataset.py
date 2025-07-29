import pandas as pd
from typing import Tuple, Optional, Union
from sklearn.model_selection import train_test_split

def split_dataset(
    dataset: pd.DataFrame,
    test_size: float = 0.2,
    random_state: Optional[int] = None,
    shuffle: bool = True
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split a dataset into training and test sets.

    Args:
        dataset (pd.DataFrame): The dataset to split
        test_size (float): Proportion of data to use for test set, default 0.2
        random_state (Optional[int]): Random seed for reproducibility
        shuffle (bool): Whether to shuffle the data before splitting

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: (train_df, test_df)

    Raises:
        ValueError: If test_size is not between 0 and 1
    """
    # Validate the test_size
    if not 0 < test_size < 1:
        raise ValueError(f"test_size must be between 0 and 1, got {test_size}")

    # Split the dataset
    train_df, test_df = train_test_split(
        dataset,
        test_size=test_size,
        random_state=random_state,
        shuffle=shuffle
    )

    return train_df, test_df