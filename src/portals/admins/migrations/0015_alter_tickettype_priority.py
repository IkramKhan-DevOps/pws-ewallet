# Generated by Django 3.2.10 on 2022-03-05 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0014_auto_20220305_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettype',
            name='priority',
            field=models.CharField(choices=[('h', 'High'), ('m', 'Medium'), ('l', 'Low')], default='m', max_length=1),
        ),
    ]
