# Generated by Django 4.2.16 on 2024-11-19 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tracker", "0014_alter_bmilog_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="goal",
            name="target_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="goal",
            name="weekly_goal",
            field=models.IntegerField(
                choices=[(1, "Lose 1 pound per week"), (2, "Lose 2 pounds per week")],
                max_length=50,
            ),
        ),
    ]
