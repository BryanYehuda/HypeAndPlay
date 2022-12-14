# Generated by Django 4.1.2 on 2022-11-11 17:52

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_adbanner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to=main.models.get_image_url)),
                ('desc', models.TextField()),
            ],
        ),
    ]
