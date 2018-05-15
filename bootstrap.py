import argparse
import coloredlogs
import logging
import pprint
import yaml

import k8s
import constants
import utils

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='inventory', required=True,
                    help='Path to inventory file')
parser.add_argument('-v', dest='verbose', action='store_true', help='Verbose output')

args = parser.parse_args()

log = logging.getLogger(__name__)
if args.verbose:
    log.setLevel(logging.DEBUG)
    level = 'DEBUG'
else:
    log.setLevel(logging.INFO)
    level = 'INFO'
coloredlogs.install(level=level)

if __name__ == '__main__':
    with open(args.inventory, 'r') as inventory_file:
        inventory = yaml.load(inventory_file)
        k8s_config = k8s.K8SConfig(**inventory['k8s'])
        nodes = utils.parse_nodes(inventory['nodes'])
        utils.parse_roles(**inventory['nodes'])
        utils.create_repo('docker.list', constants.DOCKER_REPO)
        utils.create_repo('kubernetes.list', constants.K8S_REPO)
