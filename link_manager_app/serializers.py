from rest_framework import serializers

from django.db.utils import IntegrityError

from .models import Link, Collection
from .utils import fetch_link_metadata


class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        read_only_fields = ['id', 'title', 'description', 'preview_image', 'link_type', 'created_at', 'updated_at']
        exclude = ['owner']

    def create(self, validated_data):
        url = validated_data['url']
        metadata = fetch_link_metadata(url)

        if metadata is None:
            raise serializers.ValidationError("Unable to fetch data from the provided URL.")

        link = Link(
            title=metadata["title"],
            description=metadata["description"],
            url=url,
            preview_image=metadata["preview_image"],
            link_type=metadata["link_type"],
            owner=self.context['request'].user
        )
        try:
            link.save()
        except IntegrityError:
            raise serializers.ValidationError("You can't add the same URL.")
        return link


class LinkRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        read_only_fields = ['created_at', 'updated_at']
        exclude = ['id', 'owner']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'preview_image': {'required': True},
            'link_type': {'required': True}
        }


class CollectionSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        exclude = ['owner']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        return Collection.objects.create(**validated_data, owner=self.context['request'].user)


class LinksFromCollectionSerializer(serializers.Serializer):
    link_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        write_only=True
    )

    def add(self, collection, user):
        link_ids = self.validated_data['link_ids']
        existing_links = Link.objects.filter(id__in=link_ids, owner=user)
        if not existing_links:
            raise serializers.ValidationError("No valid links found to add to the collection.")
        existing_link_ids = set(existing_links.values_list('id', flat=True))
        missing_link_ids = set(link_ids) - existing_link_ids
        collection.links.add(*existing_links)
        return {
            "added_links": len(existing_links),
            "missing_links": list(missing_link_ids)
        }

    def delete(self, collection, user):
        link_ids = self.validated_data['link_ids']
        links_to_remove = collection.links.filter(id__in=link_ids, owner=user)
        existing_link_ids = set(links_to_remove.values_list('id', flat=True))
        missing_link_ids = set(link_ids) - existing_link_ids

        if not links_to_remove:
            raise serializers.ValidationError("No valid links found to remove from the collection.")

        collection.links.remove(*links_to_remove)

        return {
            "removed_links": len(links_to_remove),
            "missing_links": list(missing_link_ids)
        }
