# Generated by Django 4.1.3 on 2022-11-28 08:02

from django.db import migrations, models
import products.storage


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_products_discount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='products_id',
            new_name='product_id',
        ),
        migrations.AlterField(
            model_name='productimages',
            name='images',
            field=models.ImageField(storage=products.storage.ProductFileStorage.imageFileStorage, upload_to='', verbose_name='Product Image'),
        ),
        migrations.AlterField(
            model_name='productreviewandratings',
            name='upload_images',
            field=models.ImageField(storage=products.storage.ProductFileStorage.imageFileStorage, upload_to='', verbose_name=''),
        ),
    ]
