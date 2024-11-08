# Generated by Django 5.1.2 on 2024-11-08 17:58

from django.db import migrations
from random import randint
from link_manager_app.test_examples import sites

users_set = ['Milasa_99', 'Zidavo_01', 'Lavora_user', 'Ladada_dev', 'Kedavo_dev', 'Lirisa_01',
             'Jotota_dev', 'Rakena_user', 'Zimosa_user', 'Najomo_01', 'Momomo_01', 'Tolula_99',
             'Jolili_01', 'Salali_app', 'Rizida_user']

collections_set = ['My Favorite Reads', 'Cooking Recipes', 'Workout Plans']


def create_test_data(apps, schema_editor):
    User = apps.get_model('user_auth', 'User')
    Collection = apps.get_model('link_manager_app', 'Collection')
    Link = apps.get_model('link_manager_app', 'Link')
    link_num = 0

    for name in users_set:
        user = User.objects.create_user(username=name, email=f"{name}@example.com", password="default_password")

        for coll_name in collections_set:
            collection = Collection.objects.create(name=coll_name, owner=user)

            for link in range(randint(3, 7)):
                link = sites[link_num]
                new_link = Link.objects.create(
                    title=link["title"],
                    description=link["description"],
                    url=link["url"],
                    preview_image=link["image"],
                    link_type=link["type"],
                    owner=user
                )
                link_num += 1
                collection.links.add(new_link)


class Migration(migrations.Migration):

    dependencies = [
        ('link_manager_app', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(create_test_data),
    ]
