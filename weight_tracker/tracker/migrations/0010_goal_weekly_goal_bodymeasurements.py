# Generated by Django 4.2.16 on 2024-11-01 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tracker", "0009_rename_current_weight_goal_start_weight"),
    ]

    operations = [
        migrations.AddField(
            model_name="goal",
            name="weekly_goal",
            field=models.CharField(
                choices=[
                    ("lose_0.5", "Lose 0.5 lbs per week"),
                    ("lose_1", "Lose 1 lb per week"),
                    ("lose_1.5", "Lose 1.5 lbs per week"),
                    ("lose_2", "Lose 2 lbs per week"),
                    ("maintain", "Maintain weight"),
                    ("gain_0.5", "Gain 0.5 lbs per week"),
                    ("gain_1", "Gain 1 lb per week"),
                ],
                default="",
                max_length=50,
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="BodyMeasurements",
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
                ("date", models.DateField(auto_now_add=True)),
                ("chest", models.FloatField()),
                ("waist", models.FloatField()),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
