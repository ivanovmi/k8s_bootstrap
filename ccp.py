import utils


@utils.execute_on_remote_label('k8s-master')
def setup_ccp():
    import subprocess
    subprocess.Popen('git clone https://github.com/openstack/fuel-ccp 2>&1 && pip install -e fuel-ccp/', shell=True)


@utils.execute_on_remote_label('k8s-master')
def deploy_local_registry():
    import subprocess
    subprocess.Popen('bash fuel-ccp/tools/registry/deploy-registry.sh', shell=True)
