# Generated by Django 5.1.3 on 2024-11-20 20:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0007_remove_tutorial_id_tutorial_plane_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Landforce',
            fields=[
                ('landforce_id', models.AutoField(primary_key=True, serialize=False)),
                ('entry_id', models.IntegerField()),
                ('unit_name', models.CharField(blank=True, max_length=255, null=True)),
                ('unit_size', models.IntegerField(blank=True, null=True)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tutorials.entities')),
            ],
            options={
                'db_table': 'landforce',
            },
        ),
        migrations.CreateModel(
            name='Plane',
            fields=[
                ('plane_id', models.AutoField(primary_key=True, serialize=False)),
                ('entry_id', models.IntegerField()),
                ('entity_id', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('enemy', models.IntegerField()),
                ('time_position', models.DateTimeField(max_length=255)),
                ('geo_altitude', models.FloatField()),
                ('velocity', models.FloatField()),
                ('true_track', models.FloatField()),
                ('call_sign', models.CharField(max_length=255)),
                ('origin_country', models.CharField(max_length=255)),
                ('on_ground', models.IntegerField()),
                ('category', models.IntegerField()),
                ('size', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'plane',
            },
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('ship_id', models.AutoField(primary_key=True, serialize=False)),
                ('entry_id', models.IntegerField()),
                ('ship_name', models.CharField(blank=True, max_length=255, null=True)),
                ('ship_type', models.CharField(blank=True, max_length=255, null=True)),
                ('displacement', models.IntegerField(blank=True, null=True)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tutorials.entities')),
            ],
            options={
                'db_table': 'ship',
            },
        ),
        migrations.DeleteModel(
            name='Tutorial',
        ),
    ]