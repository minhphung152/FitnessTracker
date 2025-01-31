# Generated by Django 4.2.16 on 2024-11-19 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("food_tracker", "0004_foodentry_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="CalculateTDEE",
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
                ("age", models.IntegerField()),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
                ("weight", models.FloatField()),
                ("height", models.FloatField()),
                (
                    "activity_level",
                    models.FloatField(
                        choices=[
                            (1.2, "Sedentary (little or no exercise)"),
                            (
                                1.375,
                                "Lightly active (light exercise/sports 1-3 days/week)",
                            ),
                            (
                                1.55,
                                "Moderately active (moderate exercise/sports 3-5 days/week)",
                            ),
                            (
                                1.725,
                                "Very active (hard exercise/sports 6-7 days a week)",
                            ),
                            (
                                1.9,
                                "Super active (very hard exercise/sports & physical job)",
                            ),
                        ]
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
