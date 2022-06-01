import logging.config
import pathlib
import yaml


proj_root = pathlib.Path(__file__).parents[2]
data_dir = proj_root / "data"
log_dir = proj_root / "logs"
conf_dir = proj_root / "config"
log_conf = conf_dir / "logging.yml"

with open(log_conf) as fin:
    config = yaml.safe_load(fin)
    logging.config.dictConfig(config)

BASE_URL = "http://localhost:3000"
