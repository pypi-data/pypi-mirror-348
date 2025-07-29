import click
from src.utils.utils import send_get, send_put, send_post, send_multipart, send_delete
import logging
import io
import mimetypes

log = logging.getLogger("immich-tools")


@click.command()
@click.argument("album_id")
@click.option("-k", "--api-key", required=True, envvar="IMMICH_API_KEY")
@click.option("-u", "--url", required=True, envvar="IMMICH_URL")
def change_owner_photo(album_id, api_key, url):
    """looking in album for specified tags and return assets without expected tags"""
    log.debug(f"immich url: {url}")
    owner_id = __get_owner_of_api_key(url, api_key)
    album_response = send_get(path=f"/api/albums/{album_id}", url=url, api_key=api_key).json()
    album_name = album_response["albumName"]
    log.debug(f"found album: {album_name}")
    assets = album_response["assets"]
    for asset in assets:
        old_asset_id = asset["id"]
        old_asset_info = send_get(path=f"/api/assets/{old_asset_id}", url=url, api_key=api_key).json()
        if old_asset_info["owner"]["id"] != owner_id:
            log.debug(f"asset: {old_asset_id} is not yours, downloading...")
            asset_content = send_get(f"/api/assets/{old_asset_id}/original", url, api_key).content
            live_video_id = asset["livePhotoVideoId"]
            if live_video_id != None:
                log.debug(f"asset have live video related: {live_video_id}, downloading...")
                live_video_asset = send_get(path=f"/api/assets/{live_video_id}", url=url, api_key=api_key).json()
                live_video_content = send_get(f"/api/assets/{live_video_id}/original", url, api_key).content
                __upload_file(url, api_key, live_video_content, live_video_asset)
            new_asset_id = __upload_file(url, api_key, asset_content, asset)
            log.debug(f"adding new asset {new_asset_id} to album...")
            send_put(f"/api/albums/{album_id}/assets", url, api_key, {"ids": [new_asset_id]})
            log.debug(f"new asset added, now removing old asset from album: {old_asset_id}")
            send_delete(f"/api/albums/{album_id}/assets", url, api_key, {"ids": [old_asset_id]})
            
            
    log.info("success")

def __get_owner_of_api_key(url: str, api_key:str):
    return send_get("/api/users/me", url, api_key).json()["id"]

def __upload_file(url: str, api_key: str, content: bytes, asset: dict):
    filename = asset["originalFileName"]
    mime_type, _ = mimetypes.guess_type(filename)
    files = {
        "assetData":  (filename, io.BytesIO(content), mime_type)
    }
    data = {
        "deviceAssetId": asset["deviceAssetId"],
        "deviceId": asset["deviceId"],
        "fileCreatedAt": asset["fileCreatedAt"],
        "fileModifiedAt": asset["fileModifiedAt"]
    }
    log.debug(f"uploading {filename}...")
    r = send_multipart("/api/assets",url, api_key, files, data)
    return r.json()["id"]