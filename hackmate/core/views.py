from django.shortcuts import render
from django.http import JsonResponse
from .models import Resource, SearchQuery
from django.db.models import Q
from .data_structures import search_queue, resource_heap, resource_trie

# Initialize trie with existing data
def initialize_data_structures():
    # Clear existing data in data structures
    resource_trie.root = resource_trie.__class__().root
    
    # Load all resources into trie and heap
    for resource in Resource.objects.all():
        # Add to trie
        for word in resource.title.split():
            resource_trie.insert(word.lower(), resource.id)
        if resource.keywords:
            for keyword in resource.keywords.split(','):
                resource_trie.insert(keyword.strip().lower(), resource.id)
        
        # Add to heap
        resource_heap.push(resource)

# Call this when Django starts
initialize_data_structures()

def home(request):
    return render(request, 'core/home.html')
def search(request):
    query = request.GET.get('q', '')
    if query:
        # Add search query to queue
        search_queue.put(query)
        SearchQuery.objects.create(query=query)
        
        # Get resource IDs from trie
        resource_ids = set()
        for word in query.lower().split():
            resource_ids.update(resource_trie.search_prefix(word))
        
        # Get matching resources
        results = Resource.objects.filter(id__in=resource_ids)
        
        # Use heap for ranking
        heap = resource_heap.__class__()
        for resource in results:
            heap.push(resource)
        
        top_results = heap.get_top_k(5)
        
        return JsonResponse({
            'results': [{
                'id': r.id,
                'title': r.title,
                'description': r.description,
                'url': r.url,
                'category': r.get_category_display(),
                'upvotes': r.upvotes,
                'keywords': r.keywords
            } for r in top_results]
        })
    return JsonResponse({'results': []})

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

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
    
# Add these imports at the top if not already present
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q

# Add this decorator to your home view
@ensure_csrf_cookie
def home(request):
    return render(request, 'core/home.html')

# Add this new view for suggestions
def search_suggestions(request):
    query = request.GET.get('q', '').lower()
    suggestions = []
    
    if query and len(query) >= 2:
        # Get suggestions from trie
        resource_ids = set()
        for word in query.split():
            resource_ids.update(resource_trie.search_prefix(word))
        
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
        suggestions = suggestions[:5]  # Limit to top 5 suggestions
    
    return JsonResponse({'suggestions': suggestions})


# Add to your existing views.py
from collections import deque
from django.db.models import F
from .models import Team

# Global team queue
team_queue = deque()

def initialize_team_queue():
    # Clear existing queue
    team_queue.clear()
    
    # Get all non-full teams and sort them by priority
    teams = Team.objects.filter(current_members__lt=F('max_members')).order_by(
        F('max_members') - F('current_members'),  # First priority: fewer spots needed
        '-max_members',  # Second priority: larger team size
        'created_at'  # Third priority: older teams first
    )
    
    # Add teams to queue
    for team in teams:
        team_queue.append(team)

# Initialize queue when Django starts
initialize_team_queue()

def get_teams(request):
    # Convert queue to list for JSON serialization
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
            if team.is_full:
                initialize_team_queue()
            
            return JsonResponse({
                'success': True,
                'current_members': team.current_members,
                'is_full': team.is_full
            })
        return JsonResponse({'success': False, 'error': 'Team is full'}, status=400)
    except Team.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Team not found'}, status=404)