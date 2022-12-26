# Generated by Django 4.1.3 on 2022-12-26 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_alter_banners_banner_images_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='category_image',
            field=models.ImageField(null=True, upload_to='category/20221226', verbose_name='category image'),
        ),
        migrations.AlterField(
            model_name='banners',
            name='banner_images',
            field=models.ImageField(upload_to='banners/20221226', verbose_name='bannerimages'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='images',
            field=models.ImageField(upload_to='product/20221226', verbose_name='Product_Image'),
        ),
        migrations.AlterField(
            model_name='productreviewandratings',
            name='upload_image',
            field=models.ImageField(null=True, upload_to='review/20221226', verbose_name='ImagesForReview'),
        ),
        migrations.AlterField(
            model_name='products',
            name='prod_mainimage',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='product/20221226', verbose_name='Product Main Image'),
        ),
    ]
