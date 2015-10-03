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


PRETTY = """
{% if short %}
<div class="codeblock" tabindex="-1">
    <pre lang="json" class="short">{{ short }}</pre>
    <pre lang="json" class="full">{{ full }}</pre>
{% else %}
<div class="codeblock">
    <pre lang="json" class="short">{{ full }}</pre>
{% endif %}
</div>
"""


def prettyprint(x):
    short = None
    full = json.dumps(json.loads(x), indent=4, ensure_ascii=False)

    lines = full.split('\n')

    if (len(lines) > 5):
        short = '\n'.join(lines[:5] + ['...'])

    return render_to_string(PRETTY,
                            {"full": full, "short": short})


class SettingsTable(tables.DataTable):

    key = tables.Column('key')
    value = tables.Column('value')

    def get_object_id(self, datum):
        return datum['key']

    class Meta:
        name = 'settings'
        table_actions = (FilterAction,)


class LeonardoTable(tables.DataTable):

    name = tables.Column('name',
                         filters=(lambda m: m.__name__,))
    widgets = tables.Column(
        'config', verbose_name=_('Widgets'),
        filters=(lambda c: ', '.join([str(w) for w in c.get('widgets', [])]),))
    plugins = tables.Column(
        'config', verbose_name=_('Plugins'),
        filters=(lambda c: ', '.join([p[0] for p in c.get('plugins', [])]),))
    live_config = tables.Column('config', filters=(lambda c: c.config, prettyprint,))

    version = tables.Column('name',
                            verbose_name=_('Version'),
                            filters=(lambda m: get_versions([m.__name__])[m.__name__],))

    def get_object_id(self, datum):
        return datum['name']

    class Meta:
        name = 'leonardo-modules'
        verbose_name = _('Leonardo Modules')
        table_actions = (FilterAction,)
