# Generated by Django 5.1.3 on 2024-11-20 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0005_alter_tutorial_geo_altitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='entry_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='time_position',
            field=models.DateTimeField(max_length=255),
        ),
    ]