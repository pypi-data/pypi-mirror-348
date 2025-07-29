import click
from src.utils.utils import send_get, send_put, send_post
import logging
from os import sys

log = logging.getLogger("immich-tools")


@click.command()
@click.argument("album_id")
@click.option("-k", "--api-key", required=True, envvar="IMMICH_API_KEY")
@click.option("-u", "--url", required=True, envvar="IMMICH_URL")
@click.option(
    "-t", "--tag", "expected_tags", required=True, multiple=True, help="expected tags (use multiple -t/--tag)"
)
@click.option("-a", "--add-missing", is_flag=True, help="will add missing tags")
@click.option("-c", "--create-tag", is_flag=True, help="will create missing tags if needed")
def check_album_tags(album_id, api_key, url, expected_tags, add_missing, create_tag):
    """looking in album for specified tags and return assets without expected tags"""
    log.debug(f"immich url: {url}")
    album_response = send_get(path=f"/api/albums/{album_id}", url=url, api_key=api_key).json()
    album_name = album_response["albumName"]
    log.debug(f"found album: {album_name}")
    assets = album_response["assets"]
    for asset in assets:
        asset_id = asset["id"]
        asset_info = send_get(path=f"/api/assets/{asset_id}", url=url, api_key=api_key).json()
        tags = [tag["value"] for tag in asset_info["tags"]]
        if not set(expected_tags).issubset(tags):
            missing_tags = list(set(expected_tags) - set(tags))
            print(f"asset: {asset_id}, actual tags: {tags}, missing tags: {missing_tags}")
            if add_missing:
                all_tags = __get_all_tags_value_id(url, api_key)
                __add_missing_tags(asset_id, missing_tags, url, api_key, all_tags, create_tag)
    log.info("success")


def __get_all_tags_value_id(url: str, api_key: str) -> dict:
    all_tags = send_get(path="/api/tags", url=url, api_key=api_key).json()
    result = {}
    for tag in all_tags:
        result[tag["value"]] = tag["id"]
    return result


def __add_missing_tags(
    asset_id: str, missing_tags: list[str], url: str, api_key: str, all_tags: dict, create_tag: bool
):
    for missing_tag in missing_tags:
        log.debug(f"adding tag: {missing_tag} to asset: {asset_id}")
        if missing_tag not in all_tags:
            if create_tag:
                log.debug(f"creating tag: {missing_tag}")
                send_post(path="/api/tags", url=url, api_key=api_key, data={"name": missing_tag})
                log.debug("retrying to add tag to asset...")
                __add_missing_tags(asset_id, missing_tags, url, api_key, __get_all_tags_value_id(url, api_key), create_tag)
                return
            else:
                log.error(f'there is not added tag "{missing_tag}" in immich. Add tag then retry.')
                sys.exit(-1)
        id = all_tags[missing_tag]
        send_put(path=f"/api/tags/{id}/assets", url=url, api_key=api_key, data={"ids": [asset_id]})
