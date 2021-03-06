# Generated by Django 3.2.9 on 2022-02-23 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20220223_2059'),
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('p2p', 'Peer To Peer')], default='p2p', max_length=3)),
                ('status', models.CharField(choices=[('com', 'Completed'), ('pen', 'Pending'), ('can', 'Cancelled')], default='pen', max_length=3)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('receiver_wallet', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver+', to='accounts.wallet')),
                ('sender_wallet', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender+', to='accounts.wallet')),
            ],
            options={
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.AlterModelOptions(
            name='withdrawal',
            options={'verbose_name_plural': 'Withdrawals'},
        ),
        migrations.AlterField(
            model_name='topup',
            name='status',
            field=models.CharField(choices=[('com', 'Completed'), ('pen', 'Pending'), ('can', 'Cancelled')], default='pen', max_length=3),
        ),
        migrations.DeleteModel(
            name='Transactions',
        ),
    ]
