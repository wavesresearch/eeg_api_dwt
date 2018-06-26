# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pymemcache.client.hash import HashClient
import os
from logger import Logger
import elasticache_auto_discovery
import socket
import warnings
from pymemcache.client.base import Client
from pymemcache.exceptions import MemcacheError


warnings.filterwarnings("ignore")
ELASTICACHE_CONFIG_ENDPOINT = os.environ.get("M_CACHED")


def memcached_conn():
    if os.environ.get('C_ENVIRONMENT', False):
        try:
            nodes = elasticache_auto_discovery.discover(ELASTICACHE_CONFIG_ENDPOINT, time_to_timeout=5)
            nodes = map(lambda x: (x[1], int(x[2])), nodes)
            memcached_client = HashClient(nodes, timeout=2, connect_timeout=2, retry_attempts=2, retry_timeout=2)
            return memcached_client
        except socket.error as e:
            Logger().log(
                Logger.ERROR,
                message="Something went wrong while connecting to memcached cluster. Reason: {}".format(e.message),
                log_now=True
            )
            return False
        except MemcacheError as e:
            Logger().log(Logger.ERROR, message="Something went wrong with memcached {}".format(e.message), log_now=True)
            return False
        except Exception as e:
            Logger().log(Logger.DEBUG, message='generic Exception: {}'.format(e.message), log_now=True)
            return False
    else:
        try:
            memcached_client = Client(('localhost', 11211))
            return memcached_client
        except MemcacheError as e:
            Logger().log(
                Logger.ERROR,
                message="Something went wrong while connecting to local memcached cluster. Reason: {}"
                    .format(e.message),
                log_now=True
            )
            return False