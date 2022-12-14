# Generated by Django 4.1 on 2022-08-07 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("repair_service", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="request",
            name="phone_model",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="request",
            name="problem_description",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="request",
            name="status",
            field=models.CharField(
                choices=[("R", "Ready"), ("W", "In work"), ("L", "In line")],
                default="L",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="request",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Invoice",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=15)),
                (
                    "request",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="repair_service.request",
                    ),
                ),
            ],
        ),
    ]
