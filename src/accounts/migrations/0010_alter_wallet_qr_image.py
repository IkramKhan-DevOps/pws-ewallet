# Generated by Django 3.2.10 on 2022-03-04 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20220304_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='qr_image',
            field=models.ImageField(blank=True, help_text='size of logo must be 200*200 and format must be png image file', null=True, upload_to='account/images/wallets/'),
        ),
    ]
