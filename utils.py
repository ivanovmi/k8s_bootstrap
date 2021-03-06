import inspect
import nodes as node_utils



roles = dict()
nodes = dict()


def parse_roles(**kwargs):
    global roles
    roles = dict()
    roles['all'] = []
    for node_name, values in kwargs.items():
        roles['all'].append(node_name)
        for label in values['labels']:
            if not roles.get(label, None):
                roles[label] = []
            roles[label].append(node_name)


def parse_nodes(_nodes):
    global nodes
    nodes = [node_utils.NodeConfig(node_name, **node_content) for node_name, node_content in _nodes.items()]
    return nodes


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


@parametrized
def execute_on_remote_label(f, label):
    def aux(*args, **kwargs):
        global nodes
        source_code = inspect.getsource(f).split('\n')
        # Remove first line in function
        source_code.pop(0)
        source_code.append('{}{}'.format(f.__name__, args))
        if source_code[0].startswith('    '):
            source_code = [x.replace('    ', '', 1) for x in source_code]
        code = '\n'.join(source_code)
        for _node in roles[label]:
            for node in nodes:
                if _node == node.name:
                    print(node.name)
                    node.ssh_client.connect(node.ip, username=node.user, key_filename=node.key)
                    stdin, stdout, stderr = node.ssh_client.exec_command('echo "{}" > run.py; python3 run.py'.format(code))
                    # FIXME
                    stderr = stderr.readlines()
                    if stderr:
                        raise Exception(stderr)
                    node.ssh_client.close()
                    sto = stdout.readlines()
        return sto[0] if len(sto) > 0 else None
    return aux


@execute_on_remote_label('all')
def create_repo(repo_name, repo_content):
    import subprocess
    subprocess.Popen('echo "{}" > /etc/apt/sources.list.d/{}'.format(repo_content, str(repo_name)), shell=True)


def install_pkgs(pkgs_list, label):
    @execute_on_remote_label(label)
    def install_pkgs_on_label(pkg_list):
        import subprocess
        subprocess.Popen('export DEBIAN_FRONTEND=noninteractive; apt-get update && apt-get install -y --allow-unauthenticated {}'.format(' '.join(pkg_list)),
                         shell=True)

    install_pkgs_on_label(pkgs_list)
