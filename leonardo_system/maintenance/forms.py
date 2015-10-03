import os

import django.dispatch
from django.conf import settings
from django.core import management
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.views.debug import get_safe_settings
from horizon import tables
from horizon_contrib.tables import FilterAction
from leonardo import forms, leonardo, messages
from leonardo.utils import get_conf_from_module

from .tables import LeonardoTable, SettingsTable

server_restart = django.dispatch.Signal(providing_args=["request", "delay"])


def server_restart_callback(request, delay=0, **kwargs):

    # time.sleep(delay)
    try:

        # from django.utils.autoreload import restart_with_reloader, reloader_thread
        # kill self
        os.kill(os.getpid(), 9)

        messages.success(
            request, _('Server was successfuly restarted !'))
    except Exception as e:
        messages.error(request, str(e))
    else:
        return True
    return False


server_restart.connect(server_restart_callback)


class ServerReloadForm(forms.SelfHandlingForm):

    delay = forms.IntegerField(
        label=_('delay before restart'), initial=10, help_text=_('Delay before restart'))

    def handle(self, request, data):
        """PoC for self restart

        this support new abilities like an dynamic plugin install etc..
        """

        try:
            server_restart.send(sender=self.__class__,
                                request=request, delay=data['delay'])
            messages.warning(
                request, _('Server going to down !'))
        except Exception as e:
            messages.error(request, str(e))
        else:
            return True
        return False


class ManagementForm(forms.SelfHandlingForm):

    """form wich handle managemenet commands

    this supports running management commands via admin
    """

    makemigrations = forms.BooleanField(
        label=_('Make migrations'), initial=False,
        required=False,
        help_text=_('Run makemigrations after install ?'))

    migrate = forms.BooleanField(
        label=_('Migrate'), initial=False,
        required=False,
        help_text=_('Run migrate command after install ?'))

    sync_all = forms.BooleanField(
        label=_('Sync All'), initial=False,
        required=False,
        help_text=_('Run Sync All command after install ?'))

    sync_force = forms.BooleanField(
        label=_('Sync all force'), initial=False,
        required=False,
        help_text=_('Warning: this may override you database changes !'),)

    reload_server = forms.BooleanField(
        label=_('Reload Server'), initial=False,
        required=False,
        help_text=_('Warning: this kill this Leonardo instance !!!\
                    For successfull reload must be run under Supervisor !\
                    You may lost your data !'),)

    def __init__(self, *args, **kwargs):
        super(ManagementForm, self).__init__(*args, **kwargs)

        self.helper.layout = forms.Layout(
            forms.TabHolder(
                forms.Tab('Main',
                          'makemigrations',
                          'migrate',
                          'sync_all',
                          css_id='plugins-install-main'
                          ),
                forms.Tab('Advance',
                          'sync_force',
                          'reload_server',
                          )
            )
        )

    def handle(self, request, data):

        try:
            if data.get('makemigrations', None):
                management.call_command(
                    'makemigrations', verbosity=1, interactive=False)
            if data.get('migrate', None):
                management.call_command(
                    'migrate', verbosity=1, interactive=False)
            if data.get('sync_all', None):
                management.call_command(
                    'sync_all', force=data.get('sync_force', False))
            if data.get('reload_server', None):
                import os
                os.kill(os.getpid(), 9)
        except Exception as e:
            messages.error(request, str(e))
        else:
            return True
        return False


class InfoForm(forms.SelfHandlingForm):

    """wrapper for system info
    """

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(InfoForm, self).__init__(*args, **kwargs)

        _settings = [{'key': k, 'value': v}
                     for k, v in six.iteritems(get_safe_settings())]

        table = SettingsTable(request, data=_settings)

        module_data = []

        for mod in getattr(settings, '_APPS', []):
            mod_cfg = get_conf_from_module(mod)
            module_data.append({
                'name': mod,
                'config': mod_cfg,
            })
        leonardo_table = LeonardoTable(request, data=leonardo.get_modules_as_list())

        self.helper.layout = forms.Layout(
            forms.TabHolder(
                forms.Tab('Settings',
                          forms.HTML(table.render())
                          ),
                forms.Tab('Leonardo modules',
                          forms.HTML(leonardo_table.render())
                          )
            )
        )

    def handle(self, request, data):
        return True
