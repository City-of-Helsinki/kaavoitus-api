# Generated by Django 2.1.4 on 2019-01-22 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0045_attribute_choice_value_textfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectphasesectionattribute',
            name='priority',
            field=models.PositiveIntegerField(default=1, verbose_name='column index'),
            preserve_default=False,
        ),
    ]