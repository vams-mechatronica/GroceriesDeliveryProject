# Generated by Django 4.1.3 on 2023-03-05 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_storeservicelocation_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Customer Name')),
                ('email', models.EmailField(blank=True, default='', max_length=254, null=True, verbose_name='Customer Email')),
                ('phone', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Customer Phone No.')),
                ('subject', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Subject')),
                ('message', models.CharField(blank=True, default='', max_length=2000, null=True, verbose_name='Message')),
            ],
        ),
    ]
