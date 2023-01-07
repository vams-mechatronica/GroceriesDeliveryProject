# Generated by Django 4.1.3 on 2023-01-07 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='long_desc',
            new_name='desc',
        ),
        migrations.RemoveField(
            model_name='products',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='products',
            name='display_name',
        ),
        migrations.RemoveField(
            model_name='products',
            name='expiry_date',
        ),
        migrations.RemoveField(
            model_name='products',
            name='flavour',
        ),
        migrations.RemoveField(
            model_name='products',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='products',
            name='item_package_quantity',
        ),
        migrations.RemoveField(
            model_name='products',
            name='manufactured_by',
        ),
        migrations.RemoveField(
            model_name='products',
            name='marketed_by',
        ),
        migrations.RemoveField(
            model_name='products',
            name='material_feature',
        ),
        migrations.RemoveField(
            model_name='products',
            name='net_content',
        ),
        migrations.RemoveField(
            model_name='products',
            name='packing_date',
        ),
        migrations.AlterField(
            model_name='banners',
            name='banner_images',
            field=models.ImageField(upload_to='banners/20230107', verbose_name='bannerimages'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='category_image',
            field=models.ImageField(blank=True, null=True, upload_to='category/20230107', verbose_name='category image'),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='images',
            field=models.ImageField(upload_to='product/20230107', verbose_name='Product_Image'),
        ),
        migrations.AlterField(
            model_name='productreviewandratings',
            name='upload_image',
            field=models.ImageField(null=True, upload_to='review/20230107', verbose_name='ImagesForReview'),
        ),
        migrations.AlterField(
            model_name='products',
            name='prod_mainimage',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='product/20230107', verbose_name='Product Main Image'),
        ),
    ]
