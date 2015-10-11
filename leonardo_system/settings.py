
from leonardo.utils.settings import dotdict

PIP_CONF = dotdict({
    'cache_dir': '/tmp',
    'trusted_hosts': ['https://pypi.python.org/pypi'],
    'index': 'https://pypi.python.org/pypi',
    'extra_index_urls': [],
    'no_index': [],
    'find_links:': []
})
