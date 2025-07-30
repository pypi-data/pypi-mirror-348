from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Start a custom Ardhi process app'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name of the New Service:')

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        os.system(f'django-admin startproject {name}')

        # Optional: Add custom views, serializers, urls, etc.
        app_path = os.path.join(os.getcwd(), name)
        with open(os.path.join(app_path, 'views.py'), 'w') as f:
            f.write("""from ardhi_framework.views import ArdhiView\n\nclass ExampleView(APIView):\n    def get(self, request):\n        return Response({'message': 'Hello from Ardhi!'})\n""")
        self.stdout.write(self.style.SUCCESS(f'Successfully created a new Ardhi based service: {name}'))
