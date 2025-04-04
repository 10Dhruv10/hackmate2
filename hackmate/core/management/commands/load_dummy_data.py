from django.core.management.base import BaseCommand
from core.models import Resource
from core.data_structures import resource_heap

class Command(BaseCommand):
    help = 'Loads dummy data for HackMate'

    def handle(self, *args, **kwargs):
        dummy_data = [
            {
                'title': 'React Weather Dashboard',
                'description': 'Build a weather dashboard using React and OpenWeather API',
                'url': 'https://github.com/example/weather-dashboard',
                'category': 'IDEA',
                'keywords': 'react, javascript, api, weather, frontend',
            },
            {
                'title': 'React Authentication Template',
                'description': 'Quick start template for React authentication using Firebase',
                'url': 'https://github.com/example/react-auth',
                'category': 'CODE',
                'keywords': 'react, authentication, firebase, template',
            },
            {
                'title': 'React State Management Guide',
                'description': 'Comprehensive guide to state management in React',
                'url': 'https://react-state-guide.com',
                'category': 'RESOURCE',
                'keywords': 'react, redux, context, state management',
            },
            {
                'title': 'AI Image Generator',
                'description': 'Create an AI-powered image generation app using DALL-E API',
                'url': 'https://github.com/example/ai-image-gen',
                'category': 'IDEA',
                'keywords': 'python, ai, image generation, api',
            },
            {
                'title': 'Python FastAPI Boilerplate',
                'description': 'Quick start template for FastAPI backend',
                'url': 'https://github.com/example/fastapi-starter',
                'category': 'CODE',
                'keywords': 'python, fastapi, backend, api',
            },
            {
                'title': 'Machine Learning Resources',
                'description': 'Curated list of ML resources for beginners',
                'url': 'https://ml-resources.com',
                'category': 'RESOURCE',
                'keywords': 'machine learning, ai, python, data science',
            },
            {
                'title': 'React Native Chat App',
                'description': 'Build a real-time chat app using React Native and Firebase',
                'url': 'https://github.com/example/react-native-chat',
                'category': 'IDEA',
                'keywords': 'react native, firebase, chat, mobile',
            },
        ]

        for data in dummy_data:
            resource = Resource.objects.create(**data)
            resource_heap.push(resource)
            self.stdout.write(self.style.SUCCESS(f'Created resource: {resource.title}'))