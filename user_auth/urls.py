from django.urls import path, include
from djoser.urls import urlpatterns as dj_url_patterns

unused_patterns = [
    'user-me',
    'user-list',
    'user-set-password',
    'user-detail',
]

base_patterns = [pattern for pattern in dj_url_patterns if pattern.name in unused_patterns]

urlpatterns = [
    path('', include(base_patterns)),
    path('auth/', include('djoser.urls.authtoken')),
]
