# Generated by Django 4.1.3 on 2023-03-05 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_order_billing_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Payment Order ID')),
                ('phone', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Buyer Phone Number')),
                ('email', models.EmailField(blank=True, default='', max_length=254, null=True, verbose_name='Buyer Email')),
                ('buyer_name', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Buyer Name')),
                ('amount', models.FloatField()),
                ('purpose', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Buyer Payment Purpose')),
                ('status', models.BooleanField(verbose_name='Payment Status')),
                ('created_at', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Payment Created At')),
                ('modified_at', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Payment Modified At')),
            ],
        ),
    ]
