# Generated by Django 4.1.3 on 2023-02-17 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_storeservicelocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeservicelocation',
            name='city',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Delivery City'),
        ),
    ]
