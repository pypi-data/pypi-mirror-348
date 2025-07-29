import boto3
import io
import pandas as pd
from typing import Literal

def resolve_dataset(
    dataset_path: str,
    bucket_type: Literal["s3"],
    dataset_format: Literal["csv"],
) -> pd.DataFrame:
    """
    Load a dataset from an S3 bucket as a pandas DataFrame.

    Args:
        dataset_path (str): Path to the dataset in S3 format (s3://bucket-name/path/to/file.csv)
        bucket_type (Literal["s3"]): Type of bucket (currently only supports 's3')
        dataset_format (Literal["csv"]): Format of the dataset (currently only supports 'csv')

    Returns:
        pd.DataFrame: The loaded dataset as a pandas DataFrame

    Raises:
        ValueError: If the bucket_type is not 's3', dataset_format is not 'csv', or the path is invalid
        ClientError: If there's an error accessing the S3 bucket
        Exception: For other errors during loading
    """
    if bucket_type != "s3":
        raise ValueError(f"Unsupported bucket type: {bucket_type}")

    if dataset_format != "csv":
        raise ValueError(f"Unsupported dataset format: {dataset_format}")

    # Parse S3 path
    if not dataset_path.startswith("s3://"):
        raise ValueError(f"Invalid S3 path format: {dataset_path}")

    # Parse bucket and key from path
    path_without_prefix = dataset_path[5:]  # Remove 's3://'
    parts = path_without_prefix.split("/", 1)
    if len(parts) < 2:
        raise ValueError(f"Invalid S3 path format: {dataset_path}")

    bucket_name, key = parts

    # Initialize S3 client
    s3_client = boto3.client("s3")

    # Download the file into a BytesIO object
    buffer = io.BytesIO()
    s3_client.download_fileobj(bucket_name, key, buffer)
    buffer.seek(0)  # Reset buffer position to the beginning

    # Load the CSV into a pandas DataFrame
    df = pd.read_csv(buffer)

    return df