import argparse
import coloredlogs
import logging
import pprint
import time
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
        log.info('Parse K8S config')
        k8s_config = k8s.K8SConfig(**inventory['k8s'])
        log.info('Parse docker config')
        docker_config = k8s.DockerConfig(**inventory['docker'])
        log.info('Parse nodes')
        nodes = utils.parse_nodes(inventory['nodes'])
        utils.parse_roles(**inventory['nodes'])
        log.info('Install {} for nodes with label {}'.format(' '.join(constants.PACKAGES), 'all'))
        utils.install_pkgs(constants.PACKAGES, 'all')
        utils.create_repo('docker.list', constants.DOCKER_REPO)
        log.info('Install {} for nodes with label {}'.format(' '.join(constants.DOCKER_PACKAGES), 'docker'))
        utils.install_pkgs(constants.DOCKER_PACKAGES, 'docker')
        log.info('Setup docker stage')
        k8s.setup_docker(docker_config.bip)
        utils.create_repo('kubernetes.list', constants.K8S_REPO)
        log.info('Install {} for nodes with label {}'.format(' '.join(constants.K8S_PACKAGES), 'k8s'))
        utils.install_pkgs(constants.K8S_PACKAGES, 'k8s')
        log.info('Init k8s master')
        join_token = k8s.init_master(k8s_config.version, k8s_config.network.cidr, k8s_config.kubelet_version)
        log.info('Init k8s network')
        k8s.init_network(k8s_config.network.provider)
        time.sleep(30)
        log.info('Init k8s worker')
        k8s.init_worker(join_token, k8s_config.kubelet_version, k8s_config.network.cidr)
        log.info('Launch k8s proxy')
        k8s.launch_kube_proxy()

