# Generated by Django 5.1.7 on 2025-03-26 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='auth',
            new_name='author',
        ),
    ]
