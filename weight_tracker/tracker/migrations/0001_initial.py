# Generated by Django 4.2.16 on 2024-10-22 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WeightLog",
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
                ("weight", models.DecimalField(decimal_places=2, max_digits=5)),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="progress_images"
                    ),
                ),
            ],
        ),
    ]
