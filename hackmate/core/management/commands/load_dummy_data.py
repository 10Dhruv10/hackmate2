from django.core.management.base import BaseCommand
from core.models import Resource
from core.data_structures import resource_heap

class Command(BaseCommand):
    help = 'Loads dummy data for HackMate'

    def handle(self, *args, **kwargs):
        # First, clear existing data
        Resource.objects.all().delete()

        dummy_data = [
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
                'title': 'AI Image Generator',
                'description': 'Create an AI-powered image generation app using DALL-E API',
                'url': 'https://github.com/example/ai-image-gen',
                'category': 'IDEA',
                'keywords': 'python,ai,image generation,api',
                'upvotes': 20
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

        for data in dummy_data:
            resource = Resource.objects.create(**data)
            resource_heap.push(resource)
            self.stdout.write(self.style.SUCCESS(f'Created resource: {resource.title}'))

from django.core.management.base import BaseCommand
from core.models import Team

class Command(BaseCommand):
    help = 'Loads dummy team data for HackMate'

    def handle(self, *args, **kwargs):
        dummy_teams = [
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
            },
            {
                'name': 'Cloud Champions',
                'description': 'Cloud computing and DevOps team',
                'max_members': 5,
                'current_members': 3,
                'contact_email': 'cloud.champions@hackmate.com',
                'contact_phone': '+1-234-567-8905',
                'contact_address': 'Cloud Center, Building E, Austin'
            },
        ]

        for data in dummy_teams:
            Team.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'Created team: {data["name"]}'))