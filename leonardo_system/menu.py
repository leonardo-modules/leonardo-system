from django.utils.translation import ugettext_lazy as _
from leonardo_admin_dashboard import modules


system_menu = modules.MenuModelList(
    _('Settings'),
    models=('constance.*', 'auth.*', 'sites.*', 'admin_sso.*',),
    order=99
)
