from __future__ import unicode_literals

from optparse import make_option

from django.conf import settings
from ._utils import get_versions, pp

from django.core.management.base import BaseCommand, NoArgsCommand


class Command(BaseCommand):

    help = "Check version of system packages"
    option_list = NoArgsCommand.option_list + (
        make_option('--leonardo',
                    action='store_false', dest='interactive', default=True,
                    help="Check just leonardo packages"),

        make_option('--noinput',
                    action='store_false', dest='interactive', default=True,
                    help="Do NOT prompt the user for input of any kind."),
    )

    def handle(self, **options):

        result = get_versions(settings.INSTALLED_APPS)

        output = pp.pprint(result)

        self.stdout.write(str(output))

        return "Needs System Update"
