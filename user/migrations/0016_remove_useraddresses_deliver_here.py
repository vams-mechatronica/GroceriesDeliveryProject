# Generated by Django 4.1.3 on 2023-03-05 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_useraddresses_deliver_here'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddresses',
            name='deliver_here',
        ),
    ]
