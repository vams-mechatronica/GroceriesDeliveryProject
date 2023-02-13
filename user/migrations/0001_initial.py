# Generated by Django 4.1.3 on 2023-02-08 03:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('mobileno', models.CharField(default='', max_length=10, unique=True, verbose_name='Mobile Number')),
                ('username', models.CharField(max_length=50, null=True, unique=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='user/20230208', verbose_name='Avatar')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(blank=True, max_length=4, null=True)),
                ('country_name', models.CharField(blank=True, max_length=50, null=True)),
                ('nick_name', models.CharField(blank=True, max_length=5, null=True)),
                ('country_image', models.CharField(blank=True, max_length=200, null=True)),
                ('country_image_2', models.ImageField(null=True, upload_to='country')),
                ('is_top', models.BooleanField(default=False, verbose_name='is_top')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
            ],
        ),
        migrations.CreateModel(
            name='UserAddresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addressLine1', models.CharField(blank=True, default='', max_length=2000, null=True, verbose_name='address line 1')),
                ('state', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='select state')),
                ('city', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='select city')),
                ('pincode', models.IntegerField(verbose_name='address pincode')),
                ('addPhoneNumber', models.CharField(blank=True, default='', max_length=13, null=True, verbose_name='address phone number')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User Detail')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceOtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('otp', models.IntegerField(blank=True, default=0, null=True)),
                ('session', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.BooleanField(default=False)),
                ('auth_token', models.UUIDField(blank=True, default=uuid.uuid4, null=True, verbose_name='auth_token')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='device_country_user', to='user.country')),
            ],
            options={
                'ordering': ('created_date',),
            },
        ),
    ]
