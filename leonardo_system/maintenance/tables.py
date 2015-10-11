import json
import os

import django.dispatch
from django.conf import settings
from django.core import management
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.views.debug import get_safe_settings
from horizon import tables
from horizon_contrib.tables import FilterAction
from leonardo import forms, messages
from leonardo.utils import get_conf_from_module
from leonardo_system.management.commands._utils import get_versions
from django.template.loader import render_to_string
import pprint

pp = pprint.PrettyPrinter(indent=4)


class SettingsTable(tables.DataTable):

    key = tables.Column('key')
    value = tables.Column('value')

    def get_object_id(self, datum):
        return datum['key']

    class Meta:
        name = 'settings'
        table_actions = (FilterAction,)


class UninstallAction(tables.DeleteAction):

    data_type_singular = 'Module'
    data_type_plural = 'Modules'
    action_present = _("Uninstall")
    action_present_plural = _("Uninstalled")

    def allowed(self, request, instance=None):
        return True

    def action(self, request, obj_id):
        raise NotImplementedError


class UpgradeAction(tables.BatchAction):

    data_type_singular = 'Module'
    data_type_plural = 'Modules'
    action_present = _("Upgrade")
    action_present_plural = _("Upgraded")
    name = 'Upgrade'

    def allowed(self, request, instance=None):
        return True

    def action(self, request, obj_id):
        raise NotImplementedError


class LeonardoTable(tables.DataTable):

    name = tables.Column('module',
                         filters=(lambda m: m.__name__,))
    widgets = tables.Column(
        'widgets', verbose_name=_('Widgets'),
        filters=(lambda c: ', '.join([str(w.__name__) for w in c]),))
    plugins = tables.Column(
        'plugins', verbose_name=_('Plugins'),
        filters=(lambda c: ', '.join([p[0] for p in c]),))

    version = tables.Column('version',
                            verbose_name=_('Version'))

    needs_migrations = tables.Column('needs_migrations',
                                     verbose_name=_('Needs Migrations'),
                                     filters=(lambda c: _(
                                         'Needs Migrations') if c else '-',)
                                     )

    needs_sync = tables.Column('needs_sync',
                               verbose_name=_('Needs Sync'),
                               filters=(lambda c: _('Needs Sync') if c else '-',))

    def get_object_id(self, datum):
        return datum.name

    class Meta:
        name = 'leonardo-modules'
        verbose_name = _('Leonardo Modules')
        row_actions = (UpgradeAction, UninstallAction,)
        table_actions = (FilterAction,)
