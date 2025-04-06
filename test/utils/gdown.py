import gdown
import os

async def download_file_from_drive(file_url, output_path):
    """
    Downloads a file from Google Drive only if it does not already exist.

    :param file_url: URL of the public file on Google Drive
    :param output_path: Path to save the downloaded file
    """
    try:
        if os.path.exists(output_path):
            print(f"File already exists: {output_path}. Skipping download.")
            return  # Skip download if the file already exists

        # Download the file using gdown
        gdown.download(file_url, output_path, quiet=False)
        print(f"File downloaded successfully to {output_path}")

    except Exception as e:
        print(f"Error downloading file: {e}")
