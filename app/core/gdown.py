import gdown

async def download_file_from_drive(file_url, output_path):
    """
    Downloads a file from Google Drive and saves it to the specified output path.

    :param file_url: URL of the public file on Google Drive
    :param output_path: Path to save the downloaded file
    """
    try:
        # Download the file using gdown
        gdown.download(file_url, output_path, quiet=False)
        print(f"File downloaded successfully to {output_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")