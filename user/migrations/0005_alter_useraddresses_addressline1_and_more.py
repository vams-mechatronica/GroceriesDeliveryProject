# Generated by Django 4.1.3 on 2023-02-15 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_useraddresses_contact_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddresses',
            name='addressLine1',
            field=models.CharField(blank=True, default=' ', max_length=2000, null=True, verbose_name='address line 1'),
        ),
        migrations.AlterField(
            model_name='useraddresses',
            name='city',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True, verbose_name='select city'),
        ),
        migrations.AlterField(
            model_name='useraddresses',
            name='mobileno',
            field=models.CharField(blank=True, default=' ', max_length=13, null=True, verbose_name='address phone number'),
        ),
        migrations.AlterField(
            model_name='useraddresses',
            name='state',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True, verbose_name='select state'),
        ),
    ]
