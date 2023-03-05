# Generated by Django 4.1.3 on 2023-03-05 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_useraddresses_area_alter_useraddresses_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddresses',
            name='apartment_name',
        ),
        migrations.RemoveField(
            model_name='useraddresses',
            name='nick_name',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user/20230305', verbose_name='Avatar'),
        ),
    ]
