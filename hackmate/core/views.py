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