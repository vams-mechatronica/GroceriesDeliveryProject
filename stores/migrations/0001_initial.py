# Generated by Django 4.1.3 on 2023-01-05 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storeName', models.CharField(default='', max_length=50, verbose_name='Store Name')),
                ('storeAddress', models.CharField(default='', max_length=250, verbose_name='Store Address')),
                ('storeLocality', models.CharField(default='', max_length=50, verbose_name='Store Locality')),
                ('storeLocalityPinCode', models.IntegerField(blank=True, null=True, verbose_name='Store Locality Pincode')),
                ('storeServicablePinCodes', models.CharField(blank=True, default='', max_length=2048, null=True, verbose_name='Store Servicable Pincodes')),
                ('storePhoneNo', models.CharField(blank=True, max_length=15, null=True, verbose_name='Store Phone No.')),
                ('storeEmail', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Store Email ID')),
                ('storeRating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, verbose_name='Store Rating')),
                ('storeStatus', models.BooleanField(default=True, verbose_name='Store Status')),
            ],
        ),
        migrations.CreateModel(
            name='StoreProductsDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Discount')),
                ('list_price', models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='Our Price')),
                ('available_stock', models.IntegerField(default=0, verbose_name='available stock')),
                ('status', models.BooleanField(default=True, verbose_name='Product Status')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products', verbose_name='store products')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.storedetail', verbose_name='Store Detail')),
            ],
        ),
    ]
