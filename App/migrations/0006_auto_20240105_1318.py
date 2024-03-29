# Generated by Django 3.2.19 on 2024-01-05 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_rename_genraid_movie_genreid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genreID',
            field=models.ForeignKey(db_column='genreID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='App.genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='releaseDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
