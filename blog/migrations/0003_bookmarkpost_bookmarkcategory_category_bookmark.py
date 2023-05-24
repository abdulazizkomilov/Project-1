# Generated by Django 4.2 on 2023-05-22 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_category_favourites'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookmarkPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'db_table': 'bookmark_post',
            },
        ),
        migrations.CreateModel(
            name='BookmarkCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'db_table': 'bookmark_category',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='bookmark',
            field=models.ManyToManyField(blank=True, default=None, related_name='bookmark', to='blog.bookmarkcategory'),
        ),
    ]
