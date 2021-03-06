# Generated by Django 3.2.12 on 2022-04-02 18:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20220402_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalaccount',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='externalaccount',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='externalaccount',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
