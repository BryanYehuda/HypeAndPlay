# Generated by Django 4.1.2 on 2022-11-16 19:15

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_adbanner"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("name", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to=main.models.get_image_url)),
                ("desc", models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name="admin",
            name="password",
            field=models.CharField(default="admin", max_length=255),
        ),
    ]
