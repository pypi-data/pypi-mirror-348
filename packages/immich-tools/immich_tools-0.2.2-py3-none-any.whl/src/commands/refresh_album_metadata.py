import click
from src.utils.utils import send_get, send_post
import logging

log = logging.getLogger("immich-tools")


@click.command()
@click.argument("album_id")
@click.option("-k", "--api-key", required=True, envvar="IMMICH_API_KEY")
@click.option("-u", "--url", required=True, envvar="IMMICH_URL")
def refresh_album_metadata(album_id, api_key, url):
    """Refresh metada in all assets in album"""
    log.debug(f"immich url: {url}")
    album_response = send_get(path=f"/api/albums/{album_id}", url=url, api_key=api_key).json()
    album_name = album_response["albumName"]
    log.debug(f"found album: {album_name}")
    assets = album_response["assets"]
    asset_ids = list()
    for asset in assets:
        asset_ids.append(asset["id"])
        data = {"assetIds": asset_ids, "name": "refresh-metadata"}
    log.debug(f"refreshing metadata for {len(assets)} assets")
    # print("essa")
    send_post("/api/assets/jobs", url, api_key, data)
    # print("Essa")
    log.info("success")
