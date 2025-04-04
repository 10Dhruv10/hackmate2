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

class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    max_members = models.IntegerField()
    current_members = models.IntegerField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    contact_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def members_needed(self):
        return self.max_members - self.current_members

    @property
    def is_full(self):
        return self.current_members >= self.max_members

    def __str__(self):
        return f"{self.name} ({self.current_members}/{self.max_members})"

class SearchQuery(models.Model):
    query = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)