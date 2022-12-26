# Generated by Django 4.1.3 on 2022-12-25 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_remove_products_discount_remove_products_expiry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banners',
            name='banner_images',
            field=models.ImageField(upload_to='banners/20221225', verbose_name='bannerimages'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='images',
            field=models.ImageField(upload_to='product/20221225', verbose_name='Product_Image'),
        ),
        migrations.AlterField(
            model_name='productreviewandratings',
            name='upload_image',
            field=models.ImageField(null=True, upload_to='review/20221225', verbose_name='ImagesForReview'),
        ),
        migrations.AlterField(
            model_name='products',
            name='prod_mainimage',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='product/20221225', verbose_name='Product Main Image'),
        ),
    ]
