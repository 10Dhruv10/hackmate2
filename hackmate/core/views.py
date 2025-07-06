from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from .models import Resource, SearchQuery
import heapq
from typing import List, Tuple

@ensure_csrf_cookie
def home(request):
    return render(request, 'core/home.html')

def convert_to_heap_entry(resource) -> Tuple[int, int, Resource]:                #i am calling those entries as resources
    return (-resource.upvotes, resource.id, resource)

def get_top_results(resources: List[Resource]) -> List[Resource]:
    # use negative upvotes for max-heap behavior
    heap_entries = [convert_to_heap_entry(r) for r in resources]                  #O(n)
    heapq.heapify(heap_entries)                                                   #O(logn)
    
    # Pop from heap to get sorted results
    sorted_results = []
    while heap_entries:
        _, _, resource = heapq.heappop(heap_entries)                              #O(nlogn)
        sorted_results.append(resource)
    
    return sorted_results

def search(request):
    query = request.GET.get('q', '').lower()
    if query:
        # Log the search query
        SearchQuery.objects.create(query=query)
        
        # Split query into words for more precise matching
        query_words = query.split()
        
        # Base query looking for matches in title or keywords
        results = Resource.objects.filter(
            Q(title__icontains=query) |
            Q(keywords__icontains=query)
        ).distinct()
        
        # Filter out less relevant results
        filtered_results = []
        for resource in results:
            title_lower = resource.title.lower()
            keywords_lower = resource.keywords.lower() if resource.keywords else ""
            
            # Check if query terms appear in title or keywords
            is_relevant = any(
                word in title_lower or 
                word in keywords_lower
                for word in query_words
            )
            
            if is_relevant:
                filtered_results.append(resource)
        

        sorted_results = get_top_results(filtered_results)             #heap comes into picture here
        
        return JsonResponse({
            'results': [{
                'id': r.id,
                'title': r.title,
                'description': r.description,
                'url': r.url,
                'category': r.get_category_display(),
                'upvotes': r.upvotes,
                'keywords': r.keywords
            } for r in sorted_results]
        })
    return JsonResponse({'results': []})

def get_top_suggestions(words: set, query: str, limit: int = 5) -> List[str]:
    """
    Use a heap to get top suggestions.
    Returns up to 'limit' suggestions that start with query.
    """
    
    heap = []                                                               #minheap
    
    for word in words:
        if word.startswith(query):
            heapq.heappush(heap, (len(word), word))
            if len(heap) > limit:
                heapq.heappop(heap)
    
    # GET the words from heap in reverse order
    return [item[1] for item in sorted(heap)]                               #i'm making it a max heap

def search_suggestions(request):
    query = request.GET.get('q', '').lower()
    suggestions = []
    
    if query and len(query) >= 2:
        resources = Resource.objects.filter(
            Q(title__icontains=query) |
            Q(keywords__icontains=query)
        ).distinct()
        
        # I am collecting words from titles and keywords here
        words = set()
        for resource in resources:
            words.update(word.lower() for word in resource.title.split())
            if resource.keywords:
                words.update(keyword.strip().lower() 
                           for keyword in resource.keywords.split(','))
        
        suggestions = get_top_suggestions(words, query, limit=5)
    
    return JsonResponse({'suggestions': suggestions})

def upvote(request, resource_id):
    try:
        resource = Resource.objects.get(id=resource_id)
        resource.upvotes += 1
        resource.save()
        return JsonResponse({'success': True, 'upvotes': resource.upvotes})
    except Resource.DoesNotExist:
        return JsonResponse({'success': False}, status=404)