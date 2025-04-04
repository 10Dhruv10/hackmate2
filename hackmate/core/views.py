from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from .models import Resource, SearchQuery

@ensure_csrf_cookie
def home(request):
    return render(request, 'core/home.html')

def search(request):
    query = request.GET.get('q', '').lower()
    if query:
        SearchQuery.objects.create(query=query)
        
        # Split query into words for more precise matching
        query_words = query.split()
        
        # Base query looking for matches in title, description, or keywords
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
        
        # Sort by upvotes
        filtered_results.sort(key=lambda x: x.upvotes, reverse=True)
        
        return JsonResponse({
            'results': [{
                'id': r.id,
                'title': r.title,
                'description': r.description,
                'url': r.url,
                'category': r.get_category_display(),
                'upvotes': r.upvotes,
                'keywords': r.keywords
            } for r in filtered_results]
        })
    return JsonResponse({'results': []})

def search_suggestions(request):
    query = request.GET.get('q', '').lower()
    suggestions = []
    
    if query and len(query) >= 2:
        resources = Resource.objects.filter(
            Q(title__icontains=query) |
            Q(keywords__icontains=query)
        ).distinct()
        
        words = set()
        for resource in resources:
            # Only add suggestions from relevant fields
            words.update(word.lower() for word in resource.title.split())
            if resource.keywords:
                words.update(keyword.strip().lower() for keyword in resource.keywords.split(','))
        
        suggestions = [word for word in words if word.startswith(query)]
        suggestions.sort()
        suggestions = suggestions[:5]
    
    return JsonResponse({'suggestions': suggestions})

def upvote(request, resource_id):
    try:
        resource = Resource.objects.get(id=resource_id)
        resource.upvotes += 1
        resource.save()
        return JsonResponse({'success': True, 'upvotes': resource.upvotes})
    except Resource.DoesNotExist:
        return JsonResponse({'success': False}, status=404)