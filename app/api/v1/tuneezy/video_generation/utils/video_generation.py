from fastapi import UploadFile


# Utility to save uploaded file
async def save_upload_file(upload_file: UploadFile, destination: str):
    with open(destination, "wb") as out_file:
        content = await upload_file.read()
        out_file.write(content)
