"""
URL configuration for link_manager_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from link_manager_app.views import LinkAPIListCreate, LinkAPIRUDView, CollectionAPIListCreate, \
    LinksFromCollectionView, CollectionAPIRUDView, TopUsersWithLinksView
from user_auth.views import UserAPIList, ResetPasswordView


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Link manager API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('user_auth.urls')),
    path('api/v1/non-auth/all-users/', UserAPIList.as_view()),
    path('api/v1/non-auth/reset-password/', ResetPasswordView.as_view()),
    path('api/v1/user/links/', LinkAPIListCreate.as_view()),
    path('api/v1/links/<int:pk>/', LinkAPIRUDView.as_view()),
    path('api/v1/user/collections/', CollectionAPIListCreate.as_view()),
    path('api/v1/collections/<int:pk>/', CollectionAPIRUDView.as_view()),
    path('api/v1/collections/<int:pk>/managing-links/', LinksFromCollectionView.as_view()),
    path('api/v1/top-users/', TopUsersWithLinksView.as_view(), name='top-users-with-links'),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
