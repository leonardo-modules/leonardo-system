
from __future__ import absolute_import

from importlib import import_module
from leonardo.utils import is_leonardo_module
from pip.commands.list import ListCommand

LEONARDO_ENV = None
GLOBAL_ENV = None


def check_versions(only_leonardo=False):
    '''returns dictionary of modules with versions to could be updated

    return:: {
            'name': {
                        'old': '1.0.1',
                        'new': '1.0.2',
                        'type': wheel
                    }
            }
    '''

    global LEONARDO_ENV
    global GLOBAL_ENV

    if only_leonardo:
        if LEONARDO_ENV:
            return LEONARDO_ENV
    else:
        if GLOBAL_ENV:
            return GLOBAL_ENV

    listing = ListCommand()
    options, args = listing.parse_args([])

    update = {}

    for dist, version, typ in listing.find_packages_latest_versions(options):
        if only_leonardo:
            pkg_names = [k for k in dist._get_metadata("top_level.txt")]
            for pkg_name in pkg_names:
                try:
                    mod = import_module(pkg_name)
                except:
                    pass
                else:
                    if is_leonardo_module(mod):
                        if version > dist.parsed_version:
                            update.update({
                                dist.project_name: {
                                    'old': dist.version,
                                    'new': version,
                                    'type': typ
                                }
                            })
        else:
            if version > dist.parsed_version:
                update.update({
                    dist.project_name: {
                        'old': dist.version,
                        'new': version,
                        'type': typ
                    }
                })

    if only_leonardo:
        LEONARDO_ENV = update
    else:
        GLOBAL_ENV = update

    return update
