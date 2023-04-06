# Generated by Django 4.1.7 on 2023-03-10 14:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('account_type', models.CharField(max_length=120)),
                ('account_no', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=22)),
                ('creation_date', models.DateTimeField()),
                ('Maturity_amount', models.DecimalField(decimal_places=2, max_digits=22)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Duration', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='Transac',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(max_length=120)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=22)),
                ('Date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Accounts_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('Date_of_birth', models.DateField()),
                ('marital_status', models.BooleanField(null=True)),
                ('Address', models.CharField(max_length=500)),
                ('aadhar', models.DecimalField(decimal_places=0, max_digits=12, unique=True)),
                ('username', models.CharField(max_length=120)),
                ('password', models.CharField(max_length=120)),
                ('secret_question', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('Mobile_number', models.BigIntegerField()),
                ('accounts', models.ManyToManyField(blank=True, null=True, to='registration.accounts')),
            ],
        ),
        migrations.AddField(
            model_name='accounts',
            name='transactions',
            field=models.ManyToManyField(blank=True, null=True, to='registration.transac'),
        ),
    ]
