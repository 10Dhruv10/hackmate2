from django.db import models

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('IDEA', 'Project Idea'),
        ('CODE', 'Code Snippet'),
        ('RESOURCE', 'Learning Resource')
    ])
    upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    keywords = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title

class SearchQuery(models.Model):
    query = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)