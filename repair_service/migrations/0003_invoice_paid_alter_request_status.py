# Generated by Django 4.1 on 2022-08-07 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "repair_service",
            "0002_request_phone_model_request_problem_description_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice", name="paid", field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="request",
            name="status",
            field=models.CharField(
                choices=[
                    ("Ready", "Ready"),
                    ("In work", "In work"),
                    ("In line", "In line"),
                ],
                default="L",
                max_length=50,
            ),
        ),
    ]
