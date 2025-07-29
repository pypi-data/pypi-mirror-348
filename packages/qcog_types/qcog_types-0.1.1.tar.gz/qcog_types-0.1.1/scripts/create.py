import json
import os
from pathlib import Path
import sys
import zipfile
import requests
import base64

def post_experiment_zip(
   base_url: str,
   *,
   folder_path: str,
   headers: dict | None = None,
):
    """
    Send an experiment.zip file to the server via POST request.

    Args:
        base_url (str): The base URL of the API
        experiment_zip_path (str): Path to the experiment.zip file
        headers (dict, optional): Additional headers to include in the request

    Returns:
        requests.Response: The response from the server
    """
    # Create the experiment.zip file
    experiment_zip_path = Path(folder_path) / "experiment.zip"
    with zipfile.ZipFile(experiment_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            # Skip __pycache__ and .venv directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.venv']]

            for file in files:
                if file == "experiment.zip":
                    continue
                print(f"Adding file: {file}")
                file_path = os.path.join(root, file)
                # Skip the zip file itself if it already exists
                if file_path == experiment_zip_path:
                    continue

                # Add file to zip with relative path
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

    print(f"Created {experiment_zip_path} with folder contents (excluding __pycache__ and .venv)")

    # Get the folder name from the experiment.zip path
    folder_name = Path(experiment_zip_path).parent
    # Search the `metadata.json` file in the folder
    metadata_path = folder_name / "metadata.json"

    if not metadata_path.exists():
        raise FileNotFoundError(f"metadata.json not found in {folder_name}")

    version: str | None = None
    name: str | None = None
    description: str | None = None
    release_notes: str | None = None
    # Read the metadata.json file

    with open(metadata_path, "r") as f:
        metadata = json.load(f)
        version = metadata.get("version")
        name = metadata.get("name")
        description = metadata.get("description")
        release_notes = metadata.get("release_notes")

    if not name:
        raise ValueError("name is required")

    if not version:
        raise ValueError("version is required")

    # Ensure the experiment.zip file exists
    if not os.path.exists(experiment_zip_path):
        raise FileNotFoundError(f"Experiment file not found: {experiment_zip_path}")

    # Construct the full URL
    url = base_url + "/experiments/upload"  # Changed to /experiments/upload to match the endpoint

    print("..:: Request to create experiment ..:: ", base_url)

    # Read the file as binary and encode as base64
    with open(experiment_zip_path, 'rb') as file:
        file_content = file.read()
        file_size = len(file_content)
        base64_encoded = base64.b64encode(file_content).decode('utf-8')

        print("..:: File ..:: ", os.path.basename(experiment_zip_path))
        print("..:: File size ..:: ", file_size)

        # Create JSON payload with all fields including base64-encoded file
        payload = {
            'experiment_file': base64_encoded,
            'experiment_name': name,
            'experiment_description': description or f"Generated experiment {name}",
            'experiment_version': version,
            'release_notes': release_notes or "",
        }

        headers = headers or {}
        headers.update({
            "Authorization": f"x-api-key {os.getenv('X_API_KEY')}",
            "Content-Type": "application/json"
        })

        print("..:: Headers ..:: ", headers)

        # Make the POST request with JSON payload
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers
            )
            print("..:: Response ..:: ", response)
            print(response.json())
            response.raise_for_status()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    # Check if the request was successful
    response.raise_for_status()

    return response

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Upload experiment.zip to server')
    parser.add_argument('--base-url', help='Base URL of the API', default="http://localhost:8001/api/v1")
    parser.add_argument('--folder-path', default='./experiment',
                        help='Path to folder to zip (default: ./experiment)')

    args = parser.parse_args()

    # Set up headers if token is provided
    headers = None
    token = os.getenv('X_API_KEY')
    if token:
        headers = {'Authorization': f'x-api-key {token}'}

    try:
        response = post_experiment_zip(
            args.base_url,
            folder_path=args.folder_path,
            headers=headers
        )
        print(f"Success! Status code: {response.status_code}")
        print("Response:")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")