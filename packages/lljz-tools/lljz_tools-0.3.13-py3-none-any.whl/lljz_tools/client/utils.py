import os
import re
import time

from lljz_tools import Color, LogManager

ssh_logger = LogManager(
    'sshtunnel', console_level='WARNING', file_path=None
).get_logger()

def parse_ssh_uri(uri: str):
    obj = re.match(
        r'^ssh://(?P<user>.+):(?P<password>.+)@(?P<host>.+?)(?::(?P<port>[0-9]+))?$', uri)
    if not obj:
        raise ValueError(f'Invalid SSH URI format: {uri}')
    ssh_config = obj.groupdict()
    if 'port' not in ssh_config:
        ssh_config['port'] = 22
    ssh_config['port'] = int(ssh_config['port'])
    return ssh_config

def setup_ssh_tunnel(host: str, port: int, ssh_uri: str):
    try:
        from sshtunnel import SSHTunnelForwarder
    except ImportError:
        raise ImportError(f'package not installed! use "{Color.color('pip install sshtunnel', style='i u yellow')}"')
    ssh_config = parse_ssh_uri(ssh_uri)
    ssh = SSHTunnelForwarder(
        ssh_address_or_host=(ssh_config['host'], ssh_config['port']),
        ssh_username=ssh_config['user'],
        ssh_password=ssh_config['password'],
        remote_bind_address=(host, port),
        logger=ssh_logger
    )
    ssh.start()
    return ssh

if __name__ == '__main__':
    # print(os.getenv('SSH_URI'))
    # es = ElasticsearchClient('es://elastic:Hoson2021@192.168.0.69:9200', os.getenv('SSH_URI'))
    # try:
    #     info = es.cluster.health()
    #     print(info)
    # except Exception as e:
    #     print("Cluster health failed:", str(e))
    ssh = setup_ssh_tunnel("192.168.0.69", 9200, os.getenv('SSH_URI'))
    print(ssh.local_bind_port)
    input()
    ssh.stop()