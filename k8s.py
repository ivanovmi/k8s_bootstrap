import constants
import utils


@utils.execute_on_remote_label('docker')
def setup_docker(docker_bip):
    import subprocess
    import json
    with open('/etc/docker/daemon.json', 'w') as of:
        json.dump({'bip': docker_bip}, of)
    subprocess.Popen('usermod -aG docker $USER && systemctl restart docker', shell=True)


@utils.execute_on_remote_label('k8s-master')
def init_master(version, cidr, kubelet_version):
    import time
    import subprocess
    process = subprocess.Popen('export DEBIAN_FRONTEND=noninteractive; apt-get install -y --allow-unauthenticated --allow-downgrades kubelet={} kubeadm={} && kubeadm init --kubernetes-version "{}" --pod-network-cidr="{}"'.format(kubelet_version, kubelet_version, version, cidr),
                               shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    out, err = process.communicate()
    print(str(out).split('\\\n')[-3].strip())
    time.sleep(60)
    subprocess.Popen('mkdir -p $HOME/.kube && cp /etc/kubernetes/admin.conf $HOME/.kube/config && chown $(id -u):$(id -g) $HOME/.kube/config', shell=True)


@utils.execute_on_remote_label('k8s-worker')
def init_worker(join_command, kubelet_version, cidr):
    import subprocess
    process = subprocess.Popen('export DEBIAN_FRONTEND=noninteractive; apt-get install -y --allow-unauthenticated --allow-downgrades kubelet={} kubeadm={} && {} --pod-network-cidr="{}"'.format(kubelet_version, kubelet_version, join_command, cidr), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    out, err = process.communicate()
    print(str(out))


def init_network(provider):
    network_url = constants.K8S_NETWORK_PROVIDERS.get(provider, None)

    @utils.execute_on_remote_label('k8s-master')
    def _init_network(network_url):
        if network_url:
            import subprocess
            subprocess.Popen('sysctl net.bridge.bridge-nf-call-iptables=1 && kubectl apply -f {}'.format(network_url), shell=True)
        else:
            raise Exception('wrong provider')
    _init_network(network_url)


@utils.execute_on_remote_label('k8s-master')
def launch_kube_proxy():
    import subprocess
    subprocess.Popen('kubectl proxy', shell=True)


class DockerConfig(object):
    def __init__(self, **kwargs):
        self.bip = kwargs['bip']


class K8SNetwork(object):
    def __init__(self, **kwargs):
        self.cidr = kwargs['cidr']
        self.provider = kwargs['provider']

    #def __repr__(self):
    #    return '\n\t'.join('{}: {}'.format(key, value) for key, value in self.__dict__.items())


class K8SConfig(object):
    def __init__(self, **kwargs):
        self.network = K8SNetwork(**kwargs['network'])
        if str(kwargs['version']) not in constants.K8S_VERSION:
            raise ValueError(kwargs['version'], constants.K8S_VERSION)
        else:
            self.version = 'stable-' + str(kwargs['version'])
            self.kubelet_version = str(kwargs['version']) + '.0-00'

    #def __repr__(self):
    #    return '\n'.join('{}: {}'.format(key, value) for key, value in self.__dict__.items())
