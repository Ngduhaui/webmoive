# Generated by Django 3.2.19 on 2024-01-03 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='moviesID',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
