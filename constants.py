# K8S constants
K8S_ROLES = ['k8s-master', 'k8s-worker', 'k8s-tainted-master']
K8S_NETWORK_PROVIDERS = {
    'calico':
        'https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/kubeadm/1.7/calico.yaml',
    'flannel':
        'https://raw.githubusercontent.com/coreos/flannel/v0.9.1/Documentation/kube-flannel.yml'
}
K8S_REPO = 'deb http://apt.kubernetes.io/ kubernetes-xenial main'
K8S_VERSION = ['1.9']
K8S_PACKAGES = ['kubelet', 'kubeadm', 'kubectl', 'kubernetes-cni']

# Docker constants
DOCKER_REPO = 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'
DOCKER_PACKAGES = ['docker-engine']

# Other constants
PACKAGES = [
    'vim', 'git', 'wget', 'tee', 'python-pip', 'python-dev', 'python3-dev', 'python-netaddr',
    'software-properties-common', 'python-setuptools', 'gcc apt-transport-https',
    'ca-certificates', 'linux-image-extra-$(uname -r)', 'linux-image-extra-virtual'
]
