from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2Widget
from leonardo import forms, messages

from .utils import pip_install, update_all


class PluginInstallForm(forms.SelfHandlingForm):
    """simple form for installing packages

    this support new abilities like an dynamic plugin install etc..
    """

    packages = forms.ChoiceField(label=_('Search packages'), widget=Select2Widget())

    reload_server = forms.BooleanField(
        label=_('Reload Server'), initial=False,
        required=False,
        help_text=_('Warning: this kill this Leonardo instance !!!\
                    For successfull reload must be run under Supervisor !\
                    You may lost your data !'),)

    def __init__(self, *args, **kwargs):
        kwargs.pop('request', None)
        super(PluginInstallForm, self).__init__(*args, **kwargs)

        self.fields['packages'].choices = [
            (repo.name, repo.name, )
            for repo in update_all()]

        self.helper.layout = forms.Layout(
            forms.TabHolder(
                forms.Tab('Main',
                          'packages',
                          css_id='plugins-install-main'
                          ),
                forms.Tab('Advance',
                          'reload_server'
                          )
            )
        )

    def handle(self, request, data):

        kwargs = data
        kwargs['request'] = request
        try:
            pip_install(**kwargs)
        except Exception as e:
            messages.error(request, str(e))
        else:
            return True
        return False
