# Generated by Django 4.1.3 on 2023-02-07 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("stores", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ordered", models.BooleanField(default=False)),
                ("quantity", models.IntegerField(default=1)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stores.storeproductsdetails",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Cart",
            },
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=15)),
                ("amount", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ref_code", models.CharField(blank=True, max_length=200, null=True)),
                ("start_date", models.DateTimeField(auto_now_add=True)),
                ("ordered_date", models.DateTimeField()),
                ("ordered", models.BooleanField(default=False)),
                (
                    "shipping_address",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="shipping_address",
                    ),
                ),
                (
                    "billing_address",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="billing_address",
                    ),
                ),
                ("being_delivered", models.BooleanField(default=False)),
                ("received", models.BooleanField(default=False)),
                ("refund_requested", models.BooleanField(default=False)),
                ("refund_granted", models.BooleanField(default=False)),
                (
                    "coupon",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="cart.coupon",
                    ),
                ),
                ("items", models.ManyToManyField(to="cart.cart")),
            ],
        ),
        migrations.CreateModel(
            name="Refund",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reason", models.TextField()),
                ("accepted", models.BooleanField(default=False)),
                ("email", models.EmailField(max_length=254)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cart.order"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("instamojo_id", models.CharField(max_length=50)),
                ("amount", models.FloatField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cart.payment",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
