from django.contrib.auth import get_user_model
from django.db.models import Count, Sum, Case, When, IntegerField

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Link, Collection
from .serializers import LinkSerializer, LinkRUDSerializer, CollectionSerializer, LinksFromCollectionSerializer

User = get_user_model()


class LinkAPIListCreate(generics.ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Link.objects.filter(owner=self.request.user)


class LinkAPIRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkRUDSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if not self.request.user.is_authenticated:  # для swagger, без этого django ругается при загрузке страницы
            return Link.objects.none()              # в браузере, но на работоспособность не влияет (можно и без этого)
        return Link.objects.filter(owner=self.request.user)


class CollectionAPIListCreate(generics.ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)


class CollectionAPIRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if not self.request.user.is_authenticated:  # для swagger, без этого django ругается при загрузке страницы
            return Collection.objects.none()        # в браузере, но на работоспособность не влияет (можно и без этого)
        return Collection.objects.filter(owner=self.request.user)


class LinksFromCollectionView(APIView):
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def check_collection(request, pk):
        try:
            collection = Collection.objects.get(pk=pk, owner=request.user)
        except Collection.DoesNotExist:
            raise NotFound("Collection not found or you do not have permission to access it.")

        return collection

    @swagger_auto_schema(request_body=LinksFromCollectionSerializer)
    def post(self, request, pk):
        collection = self.check_collection(request=request, pk=pk)

        serializer = LinksFromCollectionSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.add(collection=collection, user=request.user)
            response_data = {
                "detail": "Links added to collection successfully.",
                "added_links": result["added_links"],
                "missing_links": result["missing_links"]
            }
            if result["missing_links"]:
                response_data["detail"] = "Some links were not added because they do not exist or do not belong to you."
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=LinksFromCollectionSerializer)
    def delete(self, request, pk):
        collection = self.check_collection(request=request, pk=pk)

        serializer = LinksFromCollectionSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.delete(collection=collection, user=request.user)
            response_data = {
                "detail": "Links removed from collection successfully.",
                "removed_links": result["removed_links"],
                "missing_links": result["missing_links"]
            }
            if result["missing_links"]:
                response_data["detail"] = "Some links were not removed because they do not exist or do not belong to you."
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopUsersWithLinksView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        top_users = (
            User.objects.annotate(
                total_links=Count('links'),
                website=Sum(Case(When(links__link_type='website', then=1), output_field=IntegerField())),
                book=Sum(Case(When(links__link_type='book', then=1), output_field=IntegerField())),
                article=Sum(Case(When(links__link_type='article', then=1), output_field=IntegerField())),
                music=Sum(Case(When(links__link_type='music', then=1), output_field=IntegerField())),
                video=Sum(Case(When(links__link_type='video', then=1), output_field=IntegerField()))
            )
            .order_by('-total_links', 'date_joined')
            [:10]
            .values('email', 'total_links', 'website', 'book', 'article', 'music', 'video')
        )

        return Response(top_users)
