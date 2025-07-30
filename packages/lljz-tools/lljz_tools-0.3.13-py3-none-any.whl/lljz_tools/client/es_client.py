"""
# 手机壳es测试环境
ip：192.168.0.69:9200
账号：elastic
密码：Hoson2021

"""
import os
import re
from logging import Logger

from lljz_tools import Color, LogManager, Model

try:
    from elasticsearch import Elasticsearch
except ModuleNotFoundError:
    class Elasticsearch:

        def __init__(
                self, *args, **kwargs
        ):
            raise ModuleNotFoundError(
                f'package not installed! use "{Color.color('pip install elasticsearch', style='i u yellow')}"')


class Config(Model):
    user: str = ""
    password: str = ""
    host: str
    port: int


def parse_db_uri(uri: str) -> Config:
    """
    解析数据库连接字符串
    """
    obj = re.match(
        r'^(?P<db_type>.+)://((?P<user>.+):(?P<password>.+)@)?(?P<host>.+):(?P<port>\d+)$',
        uri
    )
    if not obj:
        raise ValueError(
            f'{uri!r} 格式错误！期望的格式为：db_type://user:password@host:port/db?qs')
    database_config = obj.groupdict()
    return Config(**database_config)  # type: ignore


sql_logger = LogManager(
    'print_sql', console_level='DEBUG', file_path=None
).get_logger()


class ElasticsearchClient(Elasticsearch):
    """
    支持ssh隧道连接，

    初始化MySQL连接池

    :param uri: ES连接字符串，格式：es://user:password@host:port
        - user: 用户名，可选
        - password: 密码，可选
        - host: 主机地址
        - port: 端口
    :param ssh_uri: SSH隧道连接字符串，格式：ssh://user:password@host:port
        - user: 用户名
        - password: 密码
        - host: 主机地址
        - port: 端口，端口可以省略，默认22
    :param show_sql: 是否显示SQL语句

    """

    def __init__(self, uri: str, ssh_uri: str | None = None, show_sql: bool | Logger = True):
        """

        """
        database_config = parse_db_uri(uri)
        if database_config.db_type.upper() != 'ES':
            raise ValueError(f'数据库类型必须为es，你输入的是{database_config.db_type!r}')
        self._ssh = None
        if show_sql is True:
            self.show_sql = sql_logger
        elif show_sql is False:
            self.show_sql = None
        else:
            self.show_sql = show_sql

        if ssh_uri:
            try:
                from lljz_tools.client.utils import setup_ssh_tunnel
            except ImportError:
                raise ImportError(
                    f'package not installed! use "{Color.color('pip install sshtunnel', style='i u yellow')}"')

            self._ssh = setup_ssh_tunnel(database_config.host, database_config.port, ssh_uri)
            database_config.host = '127.0.0.1'
            database_config.port = self._ssh.local_bind_port
        super().__init__(
            hosts=[f'http://{database_config.host}:{database_config.port}'],
            # basic_auth=(database_config.user, database_config.password) if database_config.password else None,
        )

    def close(self):
        super().close()
        if self._ssh:
            self._ssh.stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    # print(os.getenv('SSH_URI'))
    es = ElasticsearchClient(
        'es://elastic:Hoson2021@192.168.0.69:9200', os.getenv('SSH_URI')
    )
    try:
        info = es.cluster.health()
        print(info)
    except Exception as e:
        print("Cluster health failed:", str(e))

    print(es.cat.indices(format='json', h='index'))
    data = es.search(index='order_funds_detail', body={
        "query": {"match": {
          "platform_order_number.keyword": "test_SG20250517000016"
        }},
    }, size=1)
    print('search result:')
    for hits in data['hits']['hits']:
        print(hits)
