# Generated by Django 5.1.3 on 2024-11-19 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0004_alter_tutorial_time_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='geo_altitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='true_track',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='velocity',
            field=models.FloatField(),
        ),
    ]