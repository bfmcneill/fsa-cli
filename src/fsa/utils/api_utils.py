import logging
import requests
from fsa.settings import data_dir, BASE_URL

logger = logging.getLogger(__name__)


def delete_collection(collection, delay=0.05):
    """Delete all records from collection"""
    r = requests.get(f"{BASE_URL}/{collection}")
    for id in [record.get("id") for record in r.json()]:
        requests.delete(f"{BASE_URL}/{collection}/{id}")


def reset_db_json():
    """Reset API data"""
    db_json_path = data_dir / "db.json"

    # writing empty db.json
    logger.debug("writing empty db.json")
    with open(db_json_path, "w") as fout:
        fout.write('{"accounts":[],"customers":[],"ledger":[],"addresses":[]}')


if __name__ == "__main__":
    reset_db_json()
