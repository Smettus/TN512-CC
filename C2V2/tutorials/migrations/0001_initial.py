# Generated by Django 5.1.3 on 2024-11-18 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('entity_id', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('longitude',models.FloatField()),
                ('enemy', models.BooleanField()),
                ('time_position', models.DateTimeField()),
                ('geo_altitude', models.IntegerField()),
                ('velocity', models.IntegerField()),
                ('true_track', models.IntegerField()),
                ('call_sign', models.CharField(max_length=255)),
                ('origin_country', models.CharField(max_length=255)),
                ('on_ground', models.BooleanField()),
                ('category', models.IntegerField()),
                ('size', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'plane',
            },
        ),
    ]
