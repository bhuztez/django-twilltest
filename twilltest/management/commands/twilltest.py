from optparse import make_option

from django.core.management.base import BaseCommand
from ...simple import run_tests


class Command(BaseCommand):
    option_list = BaseCommand.option_list

    help = 'Runs the test suite for the specified applications, or the entire site if no apps are specified.'
    args = '[appname ...]'

    requires_model_validation = False

    def handle(self, *test_labels, **options):        
        run_tests(test_labels)

