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

        # Teams data
        teams_data = [
            {
                'name': 'AI Innovators',
                'description': 'Building next-gen AI solutions',
                'max_members': 5,
                'current_members': 4,
                'contact_email': 'ai.innovators@hackmate.com',
                'contact_phone': '+1-234-567-8901',
                'contact_address': 'Tech Hub, Building A, Silicon Valley'
            },
            {
                'name': 'Web Warriors',
                'description': 'Creating revolutionary web applications',
                'max_members': 4,
                'current_members': 3,
                'contact_email': 'web.warriors@hackmate.com',
                'contact_phone': '+1-234-567-8902',
                'contact_address': 'Innovation Center, Building B, New York'
            },
            {
                'name': 'Data Dynamos',
                'description': 'Data science and analytics experts',
                'max_members': 5,
                'current_members': 2,
                'contact_email': 'data.dynamos@hackmate.com',
                'contact_phone': '+1-234-567-8903',
                'contact_address': 'Data Park, Building C, Boston'
            },
            {
                'name': 'Mobile Mavens',
                'description': 'Mobile app development specialists',
                'max_members': 4,
                'current_members': 1,
                'contact_email': 'mobile.mavens@hackmate.com',
                'contact_phone': '+1-234-567-8904',
                'contact_address': 'App Hub, Building D, Seattle'
            }
        ]

        # Create resources
        for data in resources_data:
            Resource.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'Created resource: {data["title"]}'))

        # Create teams
        for data in teams_data:
            Team.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'Created team: {data["name"]}'))