# Generated by Django 5.1.3 on 2024-11-20 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0008_landforce_plane_ship_delete_tutorial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plane',
            name='entity_id',
            field=models.IntegerField(),
        ),
    ]
