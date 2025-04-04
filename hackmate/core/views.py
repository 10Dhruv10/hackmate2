from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Resource, SearchQuery
from .data_structures import Trie, ResourceHeap

# Global variables
resource_trie = None
resource_heap = None

def initialize_data_structures():
    """Initialize data structures lazily"""
    global resource_trie, resource_heap
    
    if resource_trie is None:
        resource_trie = Trie()
        resource_heap = ResourceHeap()
        
        try:
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
            # Handle case when database table doesn't exist yet
            pass

@ensure_csrf_cookie
def home(request):
    initialize_data_structures()  # Initialize when needed
    return render(request, 'core/home.html')

def search(request):
    initialize_data_structures()  # Initialize when needed
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
    initialize_data_structures()  # Initialize when needed
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

@csrf_protect
@require_http_methods(["POST"])
def upvote(request, resource_id):
    initialize_data_structures()  # Initialize when needed
    try:
        resource = Resource.objects.get(id=resource_id)
        resource.upvotes += 1
        resource.save()
        
        # Update resource in heap
        resource_heap.push(resource)
        
        return JsonResponse({'success': True, 'upvotes': resource.upvotes})
    except Resource.DoesNotExist:
        return JsonResponse({'success': False}, status=404)