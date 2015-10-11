from __future__ import unicode_literals

from optparse import make_option

from ._utils import pp

from django.core.management.base import BaseCommand, NoArgsCommand

from leonardo_system.pip import check_versions


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

        result = check_versions(only_leonardo=True)

        output = pp.pprint(result)

        self.stdout.write(str(output))

        return "Needs System Update"
