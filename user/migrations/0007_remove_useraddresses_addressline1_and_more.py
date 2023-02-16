# Generated by Django 4.1.3 on 2023-02-16 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_useraddresses_unique_primary_per_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddresses',
            name='addressLine1',
        ),
        migrations.RemoveField(
            model_name='useraddresses',
            name='address_name',
        ),
        migrations.RemoveField(
            model_name='useraddresses',
            name='contact_name',
        ),
        migrations.AddField(
            model_name='useraddresses',
            name='address_nick_name',
            field=models.CharField(blank=True, choices=[('Home', 'Home'), ('Office', 'Office'), ('Others', 'Others')], default='Home', max_length=50, null=True, verbose_name='Address Nick Name'),
        ),
        migrations.AddField(
            model_name='useraddresses',
            name='apartment_name',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Apartment Name'),
        ),
        migrations.AddField(
            model_name='useraddresses',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Address First Name'),
        ),
        migrations.AddField(
            model_name='useraddresses',
            name='house_no',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='House No'),
        ),
        migrations.AddField(
            model_name='useraddresses',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Address Last Name'),
        ),
        migrations.AddField(
            model_name='useraddresses',
            name='nick_name',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Contact Nick Name'),
        ),
        migrations.AddField(
            model_name='useraddresses',
            name='street_detail',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Street Detail'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user/20230216', verbose_name='Avatar'),
        ),
    ]
