# Generated by Django 4.1.7 on 2023-04-03 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_accounts_list_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts_list',
            name='Date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
