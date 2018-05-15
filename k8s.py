import constants
import utils


@utils.execute_on_remote_label('docker')
def setup_docker():
    pass


@utils.execute_on_remote_label('k8s-tainted-master')
def taint_node():
    pass


def setup_kubeconfig():
    pass


class K8SNetwork(object):
    def __init__(self, **kwargs):
        self.cidr = kwargs['cidr']
        self.provider = kwargs['provider']

    def __repr__(self):
        return '\n\t'.join('{}: {}'.format(key, value) for key, value in self.__dict__.items())


class K8SConfig(object):
    def __init__(self, **kwargs):
        self.network = K8SNetwork(**kwargs['network'])
        if str(kwargs['version']) not in constants.K8S_VERSION:
            raise ValueError(kwargs['version'], constants.K8S_VERSION)
        else:
            self.version = 'stable-' + str(kwargs['version'])
            self.kubelet_version = str(kwargs['version'])

    def __repr__(self):
        return '\n'.join('{}: {}'.format(key, value) for key, value in self.__dict__.items())