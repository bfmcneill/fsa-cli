import logging
import click

from fsa.utils import api_utils
from fsa.utils import fs_utils

logger = logging.getLogger(__name__)


@click.group
def commands():
    """util commands"""


@commands.command
def reset_db_json():
    api_utils.reset_db_json()


@commands.command()
def rm_logs():
    fs_utils.delete_log_files()
