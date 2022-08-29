from django.core.management.base import BaseCommand

from NewsPaper.news.models import Post, Category


class Command(BaseCommand):
    help = 'Delete all news from chosen Category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Are you sure you want to delete all news from {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Cancelled'))

        try:
            category = Category.get(name=options['category'])
            Post.objects.filter(category == category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Successfully deleted all news from {category.name}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category'))
