# Generated by Django 4.2.16 on 2024-11-22 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("food_tracker", "0008_remove_foodentry_calories_unit_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="foodentry",
            options={"verbose_name_plural": "Food Entries"},
        ),
        migrations.AddField(
            model_name="foodentry",
            name="servings",
            field=models.FloatField(default=1),
        ),
    ]
