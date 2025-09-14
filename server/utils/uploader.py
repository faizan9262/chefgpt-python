import cloudinary.uploader
from fastapi import UploadFile

# Upload file buffer (e.g. real uploads from client)
async def upload_file_to_cloudinary(file: UploadFile, folder="ChefGPT") -> str:
    file_content = await file.read()
    result = cloudinary.uploader.upload(file_content, folder=folder)
    return result["secure_url"]


# Upload directly from URL or base64 string
def upload_from_url_or_base64(image_url: str, folder="ChefGPT") -> str:
    result = cloudinary.uploader.upload(image_url, folder=folder)
    return result["secure_url"]
