# Generated by Django 2.1.2 on 2018-11-21 08:08

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0030_increase_filename_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectSubtype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='metadata')),
                ('index', models.PositiveIntegerField(verbose_name='index')),
                ('project_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtypes', to='projects.ProjectType', verbose_name='project type')),
            ],
            options={
                'verbose_name': 'project subtype',
                'verbose_name_plural': 'project subtypes',
                'ordering': ('index',),
            },
        ),
        migrations.RemoveField(
            model_name='project',
            name='type',
        ),
        migrations.RemoveField(
            model_name='projectphase',
            name='project_type',
        ),
        migrations.AddField(
            model_name='project',
            name='subtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='projects.ProjectSubtype', verbose_name='subtype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectphase',
            name='project_subtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phases', to='projects.ProjectSubtype', verbose_name='project type'),
            preserve_default=False,
        ),
    ]
