# Generated by Django 3.1.6 on 2021-04-26 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common_auth', '0003_extauthcred_host_spec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='access_kaavapino',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='access_kaavapino_creds', to='common_auth.extauthcred', verbose_name='Kaavapino'),
        ),
    ]
