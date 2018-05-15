import paramiko


class NodeConfig(object):
    def __init__(self, node_name, **kwargs):
        self.name = node_name
        self.ip = kwargs['ip']
        self.user = kwargs['username']
        self.key = kwargs['identity_file']
        self.roles = kwargs['roles'] if kwargs.get('roles') else []
        self.labels = kwargs['labels'] if kwargs.get('labels') else []
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __repr__(self):
        return '\n'.join('{}: {}'.format(key, value) for key, value in self.__dict__.items())
