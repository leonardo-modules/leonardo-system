
from __future__ import absolute_import

from constance.admin import ConstanceForm
from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers
from leonardo.views import *
from leonardo.views import ModalFormView
from constance import settings, LazyConfig
from .forms import InfoForm, ManagementForm, ServerReloadForm

config = LazyConfig()


class ServerReloadView(ModalFormView, ContextMixin, ModelFormMixin):

    form_class = ServerReloadForm

    def get_success_url(self):
        return self.request.build_absolute_uri()

    def get_context_data(self, **kwargs):
        context = super(ServerReloadView, self).get_context_data(**kwargs)

        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = 'Reload Server'
        context['title'] = 'Reload Server'
        context['form_submit'] = _('Submit Reload')
        context['heading'] = 'Reload Server'
        context['modal_size'] = 'sm'
        return context


class InfoView(ModalFormView, ContextMixin, ModelFormMixin):

    form_class = InfoForm

    def get_success_url(self):
        return self.request.build_absolute_uri()

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""

        kwargs = self.get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return form_class(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(InfoView, self).get_context_data(**kwargs)

        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = _('Leonardo Info')
        context['title'] = _('Leonardo Info')
        context['form_submit'] = _('Close')
        context['heading'] = _('Leonardo Info')
        context['modal_size'] = 'fullscreen'
        return context

    def form_invalid(self, form):
        raise Exception(form.errors)


class ManagementView(ModalFormView, ContextMixin, ModelFormMixin):

    form_class = ManagementForm

    def get_success_url(self):
        return self.request.build_absolute_uri()

    def get_context_data(self, **kwargs):
        context = super(ManagementView, self).get_context_data(**kwargs)

        context['url'] = self.request.build_absolute_uri()
        context['modal_header'] = _('Management commands')
        context['title'] = _('Management commands')
        context['form_submit'] = _('Run commands')
        context['heading'] = _('Management commands')
        context['modal_size'] = 'md'
        return context

    def form_invalid(self, form):
        raise Exception(form.errors)


class ConfigUpdate(ModalFormView):

    form_class = ConstanceForm

    success_url = "feincms_home"

    def get_context_data(self, *args, **kwargs):
        context = super(ConfigUpdate, self).get_context_data(*args, **kwargs)
        context['modal_size'] = 'lg'
        return context

    def get_success_url(self):
        return urlresolvers.reverse(self.success_url)

    def get_initial(self):
        default_initial = ((name, default)
                           for name, (default, help_text) in settings.CONFIG.items())
        # Then update the mapping with actually values from the backend
        initial = dict(default_initial,
                       **dict(config._backend.mget(settings.CONFIG.keys())))
        return initial
