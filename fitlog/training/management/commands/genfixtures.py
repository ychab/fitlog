from django.core.management.base import BaseCommand

from ...fixtures import create_fixtures
from ...models import Exercise, Routine, Training


class Command(BaseCommand):
    help = 'Generate some trainings for a demo purpose.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            action='store',
            type=int,
            default=10,
            help="How many trainings to generate",
        )
        parser.add_argument(
            '--testing',
            action='store_true',
            default=False,
            help="Whether to also generate demo data (trainings with sets) or not.",
        )
        parser.add_argument(
            '--purge',
            action='store_true',
            default=False,
            help="Whether to delete all previous trainings before creating new ones.",
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            default=False,
            help="Whether to delete all model instances (routines, exercises, etc).",
        )

    def handle(self, *args, **options):

        if options.get('reset'):
            confirm = input('Are you sure you want to delete all instances? (Y/n)')
            if confirm == 'n':
                return

            Routine.objects.all().delete()
            Exercise.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('All previous model instances have been deleted.'),
            )

        elif options.get('purge'):
            Training.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('All previous trainings have been deleted.'),
            )

        create_fixtures(limit=options['limit'], testing=options['testing'])

        self.stdout.write(
            self.style.SUCCESS('Data generated successfully.',),
        )
