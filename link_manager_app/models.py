from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Link(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    preview_image = models.URLField(blank=True, null=True)
    link_type = models.CharField(max_length=30, default='website')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'url'], name='unique_url_for_user')
        ]

    def __str__(self):
        return self.title


class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    links = models.ManyToManyField(Link, related_name='collections')

    def __str__(self):
        return self.name
