
from __future__ import absolute_import

from django.apps import AppConfig


default_app_config = 'leonardo_system.Config'


LEONARDO_APPS = ['leonardo_system']
LEONARDO_OPTGROUP = 'System'
LEONARDO_URLS_CONF = 'leonardo_system.urls'
LEONARDO_PAGE_ACTIONS = ['system/module_actions.html']
LEONARDO_ORDERING = 150


class Config(AppConfig):
    name = 'leonardo_system'
    verbose_name = "Leonardo System Module"

    def ready(self):

        try:

            from leonardo_system.package.patch_pip import indent_log
            from pip.req import req_set
            req_set.indent_log = indent_log
        except Exception as e:
            raise e
