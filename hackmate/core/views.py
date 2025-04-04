from django.shortcuts import render
from django.http import JsonResponse
from .models import Resource, SearchQuery
from django.db.models import Q
from .data_structures import search_queue, resource_heap, resource_trie

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
        for word in query.split():
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