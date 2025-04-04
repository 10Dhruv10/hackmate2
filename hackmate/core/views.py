from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_http_methods
from django.db.models import F, Q
from collections import deque
from .models import Resource, SearchQuery, Team
from .data_structures import Trie, ResourceHeap

# Global variables
resource_trie = Trie()
resource_heap = ResourceHeap()
team_queue = deque()
is_queue_initialized = False

def initialize_data_structures():
    """Initialize data structures lazily"""
    try:
        # Initialize resource data structures
        for resource in Resource.objects.all():
            # Add to trie
            for word in resource.title.split():
                resource_trie.insert(word.lower(), resource.id)
            if resource.keywords:
                for keyword in resource.keywords.split(','):
                    resource_trie.insert(keyword.strip().lower(), resource.id)
            
            # Add to heap
            resource_heap.push(resource)
    except:
        pass

def initialize_team_queue():
    """Initialize the team queue if not already initialized"""
    global team_queue, is_queue_initialized
    try:
        if not is_queue_initialized:
            team_queue.clear()
            teams = Team.objects.filter(current_members__lt=F('max_members')).order_by(
                F('max_members') - F('current_members'),
                '-max_members',
                'created_at'
            )
            for team in teams:
                team_queue.append(team)
            is_queue_initialized = True
    except:
        pass

@ensure_csrf_cookie
def home(request):
    return render(request, 'core/home.html')

def search(request):
    query = request.GET.get('q', '')
    if query:
        SearchQuery.objects.create(query=query)
        
        # Get resource IDs from trie
        resource_ids = set()
        for word in query.lower().split():
            resource_ids.update(resource_trie.search_prefix(word))
        
        # Get matching resources
        results = Resource.objects.filter(id__in=resource_ids)
        
        return JsonResponse({
            'results': [{
                'id': r.id,
                'title': r.title,
                'description': r.description,
                'url': r.url,
                'category': r.get_category_display(),
                'upvotes': r.upvotes,
                'keywords': r.keywords
            } for r in results]
        })
    return JsonResponse({'results': []})

def search_suggestions(request):
    query = request.GET.get('q', '').lower()
    suggestions = []
    
    if query and len(query) >= 2:
        # Get suggestions from trie
        resource_ids = set()
        resource_ids.update(resource_trie.search_prefix(query))
        
        # Get matching resources
        resources = Resource.objects.filter(id__in=resource_ids)
        
        # Extract unique words from titles and keywords
        words = set()
        for resource in resources:
            words.update(word.lower() for word in resource.title.split())
            if resource.keywords:
                words.update(keyword.strip().lower() for keyword in resource.keywords.split(','))
        
        # Filter suggestions that start with the query
        suggestions = [word for word in words if word.startswith(query)]
        suggestions.sort()
        suggestions = suggestions[:5]
    
    return JsonResponse({'suggestions': suggestions})

def get_teams(request):
    initialize_team_queue()
    teams_list = list(team_queue)
    return JsonResponse({
        'teams': [{
            'id': team.id,
            'name': team.name,
            'description': team.description,
            'max_members': team.max_members,
            'current_members': team.current_members,
            'members_needed': team.members_needed,
            'contact_email': team.contact_email,
            'contact_phone': team.contact_phone,
            'contact_address': team.contact_address,
        } for team in teams_list]
    })

@csrf_protect
@require_http_methods(["POST"])
def join_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
        if not team.is_full:
            team.current_members += 1
            team.save()
            
            # Reinitialize queue if team is now full
            global is_queue_initialized
            is_queue_initialized = False
            initialize_team_queue()
            
            return JsonResponse({
                'success': True,
                'current_members': team.current_members,
                'is_full': team.is_full
            })
        return JsonResponse({'success': False, 'error': 'Team is full'}, status=400)
    except Team.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Team not found'}, status=404)

@csrf_protect
@require_http_methods(["POST"])
def upvote(request, resource_id):
    try:
        resource = Resource.objects.get(id=resource_id)
        resource.upvotes += 1
        resource.save()
        
        # Update resource in heap
        resource_heap.push(resource)
        
        return JsonResponse({'success': True, 'upvotes': resource.upvotes})
    except Resource.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

# Initialize data structures when the module loads
initialize_data_structures()