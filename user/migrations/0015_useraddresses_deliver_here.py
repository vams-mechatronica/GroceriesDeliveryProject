# Generated by Django 4.1.3 on 2023-03-05 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_remove_useraddresses_apartment_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddresses',
            name='deliver_here',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Deliver Here'),
        ),
    ]
