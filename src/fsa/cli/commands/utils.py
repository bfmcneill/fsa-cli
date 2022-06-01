import logging
import click

from fsa.utils import api_utils
from fsa.utils import fs_utils

logger = logging.getLogger(__name__)


@click.group
def commands():
    """Developer utilities"""


@commands.command
def reset_db_json():
    """Destructive operation that resets `db.json`"""
    api_utils.reset_db_json()


@commands.command()
def rm_logs():
    """Destructive operation that removes all .log files from `logs` directory"""
    fs_utils.delete_log_files()
