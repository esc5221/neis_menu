# Generated by Django 4.0.6 on 2022-08-12 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    # replaces = [('menus', '0001_initial'), ('menus', '0002_menu_calories_menu_dishes'), ('menus', '0003_alter_menu_dishes')]

    initial = True

    dependencies = [
        ("schools", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Menu",
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
                (
                    "type",
                    models.IntegerField(choices=[(1, "아침"), (2, "점심"), (3, "저녁")]),
                ),
                ("date", models.DateField()),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="schools.school"
                    ),
                ),
                ("calories", models.PositiveIntegerField(null=True)),
                ("dishes", models.CharField(blank=True, max_length=500)),
            ],
        ),
    ]
