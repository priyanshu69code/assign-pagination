from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Article
import random
import requests


class Command(BaseCommand):
    help = 'Populate the database with sample articles'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, help='Number of Articles to Create(default to 50)', default=50)


    def handle(self, *args, **kwargs):
        count = kwargs['count']

        data = requests.get('https://jsonplaceholder.typicode.com/posts')
        print(data)
