import click
from src.commands import merge_xmp, refresh_album_metadata, run_job, version, check_album_tags, change_owner_photo
import logging
from datetime import datetime
import src


log = logging.getLogger("immich-tools")
log.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)-5s - %(message)s")


console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

log.addHandler(console_handler)


@click.group(help=f"""This is immich-tools version {src.__version__}""")
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode")
@click.option("-l", "--log-file", is_flag=True, help="Saves logs to file")
@click.option(
    "--log-path", help="path to directory where logs will be stored, works only if --log-file flag is set to True"
)
@click.pass_context
def main(ctx, debug: bool, log_file: bool, log_path: str):
    f"""Tools for immich, version """
    ctx.ensure_object(dict)
    log.info("Running immich-tools")
    if log_file:
        log_directory = log_path if log_path else "."
        file_handler = logging.FileHandler(datetime.now().strftime(f"{log_directory}/log_%d_%m_%Y.log"))
        file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
    if debug:
        log.setLevel(logging.DEBUG)
        log.debug("Debug mode is ON")


main.add_command(refresh_album_metadata.refresh_album_metadata)
main.add_command(merge_xmp.merge_xmp)
main.add_command(run_job.run_job)
main.add_command(version.version)
main.add_command(check_album_tags.check_album_tags)
main.add_command(change_owner_photo.change_owner_photo)
