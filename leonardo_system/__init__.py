
from django.apps import AppConfig


default_app_config = 'leonardo_system.Config'


LEONARDO_APPS = ['leonardo_system']
LEONARDO_OPTGROUP = 'System'
LEONARDO_URLS_CONF = 'leonardo_system.urls'
LEONARDO_MODULE_ACTIONS = ['system/module_actions.html']
LEONARDO_ORDERING = 150


class Config(AppConfig):
    name = 'leonardo_system'
    verbose_name = "Leonardo System Module"
