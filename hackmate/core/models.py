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
    keywords = models.CharField(max_length=500, blank=True, help_text="Comma-separated keywords")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            from .data_structures import resource_trie
            # Index the title and keywords in the trie
            for word in self.title.split():
                resource_trie.insert(word, self.id)
            if self.keywords:
                for keyword in self.keywords.split(','):
                    resource_trie.insert(keyword.strip(), self.id)

    def __str__(self):
        return self.title

class SearchQuery(models.Model):
    query = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)