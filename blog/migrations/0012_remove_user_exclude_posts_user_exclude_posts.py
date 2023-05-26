# Generated by Django 4.0 on 2023-05-26 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_user_exclude_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='exclude_posts',
        ),
        migrations.AddField(
            model_name='user',
            name='exclude_posts',
            field=models.ManyToManyField(blank=True, to='blog.Post'),
        ),
    ]
