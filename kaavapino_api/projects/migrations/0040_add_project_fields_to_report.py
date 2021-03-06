# Generated by Django 2.1.2 on 2018-12-17 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0039_project_geometries'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='show_created_at',
            field=models.BooleanField(default=False, verbose_name='show created at on report'),
        ),
        migrations.AddField(
            model_name='report',
            name='show_modified_at',
            field=models.BooleanField(default=False, verbose_name='show modified at on report'),
        ),
        migrations.AddField(
            model_name='report',
            name='show_name',
            field=models.BooleanField(default=False, verbose_name='show name on report'),
        ),
        migrations.AddField(
            model_name='report',
            name='show_phase',
            field=models.BooleanField(default=False, verbose_name='show phase on report'),
        ),
        migrations.AddField(
            model_name='report',
            name='show_subtype',
            field=models.BooleanField(default=False, verbose_name='show subtype on report'),
        ),
        migrations.AddField(
            model_name='report',
            name='show_user',
            field=models.BooleanField(default=False, verbose_name='show user on report'),
        ),
    ]
