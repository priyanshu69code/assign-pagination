from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Article
import random
import requests
from faker import Faker


class Command(BaseCommand):
    help = 'Populate the database with sample articles'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, help='Number of Articles to Create(default to 50)', default=50)


    def handle(self, *args, **kwargs):
        count = kwargs['count']

        fake = Faker()
        for _ in range(count):
            Article.objects.create(
                title=fake.sentence(),
                content=fake.text(),
                author=fake.name(),
                is_published=random.choice([True, False])
            )
        self.stdout.write(self.style.SUCCESS(f'Created {count} articles.'))
