from utils.const import UPLOAD_PHOTO_URL
import requests


async def upload_image_to_img_server(file):
    result = requests.post(UPLOAD_PHOTO_URL, files={"image": file})
    return result.json()["data"]["url"]
