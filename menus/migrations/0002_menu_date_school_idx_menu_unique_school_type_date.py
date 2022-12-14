# Generated by Django 4.0.6 on 2022-08-11 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menus", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="menu",
            index=models.Index(fields=["date", "school"], name="date_school_idx"),
        ),
        migrations.AddConstraint(
            model_name="menu",
            constraint=models.UniqueConstraint(
                fields=("school", "type", "date"), name="unique_school_type_date"
            ),
        ),
    ]
