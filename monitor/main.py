import argparse
import json
from datetime import datetime
import yaml
import sys
import time
import logging
from typing import Dict, Any

from pykwalify.core import Core
from pykwalify.errors import SchemaError

from monitor.monitor import monitor_endpoints
from monitor.serializer import json_serial
from monitor.utils import clean_url
from monitor.metrics import HealthMetrics


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()

# handler level is different from logger level
handler.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def read_config(file_path: str) -> Dict[str, Any]:
    """
    Read and parse a YAML configuration file.

    :param file_path: Path to the YAML configuration file
    :return: Dictionary containing the configuration
    :raises: FileNotFoundError if file doesn't exist
    :raises: yaml.YAMLError if file is invalid YAML
    """
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(
            f"Error: Configuration file '{file_path}' not found", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(
            f"Error: Invalid YAML in configuration file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Monitor endpoints from a YAML configuration file')
    parser.add_argument(
        'config_file', help='Path to the YAML configuration file')
    args = parser.parse_args()

    config = read_config(args.config_file)

    core = Core(source_data=config,
                schema_files=["config-schema.yaml"])
    try:
        core.validate()
    except SchemaError as e:
        logger.error("Validation failed:")
        for err in e.args[0]:
            logger.error("  ", err)

    for item in config:
        item['url'] = clean_url(item['url'])
        if 'method' not in item:
            item['method'] = 'GET'
        if 'body' not in item:
            item['body'] = None
        if 'headers' not in item:
            item['headers'] = {}
    # TODO detect duplicates
    print(config)

    health_metrics = HealthMetrics()
    stats = {'start': datetime.now()}
    while True:
        start_time = time.time()
        stats = monitor_endpoints(config, stats, health_metrics)
        elapsed = time.time() - start_time
        if elapsed > 15:
            logger.error(
                f"Monitoring cycle took {elapsed:.2f} seconds, exceeding 15 second threshold")
            sys.exit(-1)
        logger.info(json.dumps(stats, indent=4,
                    sort_keys=True, default=json_serial))


if __name__ == '__main__':
    main()
