from django.core.management.base import BaseCommand
from core.models import Resource, Team

class Command(BaseCommand):
    help = 'Loads all dummy data for HackMate'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Resource.objects.all().delete()
        Team.objects.all().delete()

        # Resources data
        resources_data = [
            {
                'title': 'React Weather Dashboard',
                'description': 'Build a weather dashboard using React and OpenWeather API',
                'url': 'https://github.com/example/weather-dashboard',
                'category': 'IDEA',
                'keywords': 'react,javascript,api,weather,frontend',
                'upvotes': 15
            },
            {
                'title': 'React Authentication Template',
                'description': 'Quick start template for React authentication using Firebase',
                'url': 'https://github.com/example/react-auth',
                'category': 'CODE',
                'keywords': 'react,authentication,firebase,template',
                'upvotes': 25
            },
            {
                'title': 'React State Management Guide',
                'description': 'Comprehensive guide to state management in React',
                'url': 'https://react-state-guide.com',
                'category': 'RESOURCE',
                'keywords': 'react,redux,context,state management',
                'upvotes': 30
            },
            {
                'title': 'Python FastAPI Boilerplate',
                'description': 'Quick start template for FastAPI backend',
                'url': 'https://github.com/example/fastapi-starter',
                'category': 'CODE',
                'keywords': 'python,fastapi,backend,api',
                'upvotes': 18
            }
        ]

      

        # Create resources
        for data in resources_data:
            Resource.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'Created resource: {data["title"]}'))
