# Generated by Django 2.1.1 on 2018-09-10 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='movie',
            new_name='movie_id',
        ),
    ]
