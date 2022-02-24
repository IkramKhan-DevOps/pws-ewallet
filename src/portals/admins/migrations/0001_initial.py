# Generated by Django 3.2.9 on 2022-02-23 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0005_auto_20220223_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.CharField(default='bx bx-transfer', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Payment Methods',
            },
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('bank_name', models.CharField(max_length=1000)),
                ('bank_branch', models.CharField(max_length=1000)),
                ('bank_account_number', models.CharField(max_length=1000)),
                ('status', models.CharField(choices=[('com', 'Completed'), ('pen', 'Pending'), ('can', 'Cancelled')], max_length=3)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('wallet', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.wallet')),
            ],
            options={
                'verbose_name_plural': 'Top Ups',
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('p2p', 'Peer To Peer')], max_length=3)),
                ('status', models.CharField(choices=[('com', 'Completed'), ('pen', 'Pending'), ('can', 'Cancelled')], max_length=3)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('receiver_wallet', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver+', to='accounts.wallet')),
                ('sender_wallet', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender+', to='accounts.wallet')),
            ],
            options={
                'verbose_name_plural': 'Top Ups',
            },
        ),
        migrations.CreateModel(
            name='TopUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('com', 'Completed'), ('pen', 'Pending'), ('can', 'Cancelled')], max_length=3)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('wallet', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.wallet')),
            ],
            options={
                'verbose_name_plural': 'Top Ups',
            },
        ),
    ]