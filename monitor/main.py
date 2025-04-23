import argparse
import json
from datetime import datetime, date

import yaml
import sys
import time
import logging
from typing import Dict, Any

from monitor.monitor import monitor_endpoints
from monitor.serializer import json_serial
from monitor.utils import clean_url


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
        print(f"Error: Configuration file '{file_path}' not found", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in configuration file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Monitor endpoints from a YAML configuration file')
    parser.add_argument('config_file', help='Path to the YAML configuration file')
    args = parser.parse_args()
    
    config = read_config(args.config_file)
    for item in config:
        if 'url' not in item:
            print(f"Error: Missing 'url' in configuration item: {item}", file=sys.stderr)
            sys.exit(1)
        item['url'] = clean_url(item['url'])
        if 'method' not in item:
            item['method'] = 'GET'
        if 'body' not in item:
            item['body'] = None
        if 'headers' not in item:
            item['headers'] = {}
    # TODO detect duplicates
    print(config)

    stats = {'start': datetime.now()}
    while True:
        start_time = time.time()
        stats = monitor_endpoints(config, stats)
        elapsed = time.time() - start_time
        if elapsed > 15:
            logger.error(f"Monitoring cycle took {elapsed:.2f} seconds, exceeding 15 second threshold")
        logger.info(json.dumps(stats, indent=4, sort_keys=True, default=json_serial))

if __name__ == '__main__':
    main()


