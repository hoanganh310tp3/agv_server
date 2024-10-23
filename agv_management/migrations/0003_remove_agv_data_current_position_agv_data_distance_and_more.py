# Generated by Django 5.0.3 on 2024-10-23 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agv_management', '0002_position_remove_agv_data_distance_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agv_data',
            name='current_position',
        ),
        migrations.AddField(
            model_name='agv_data',
            name='distance',
            field=models.FloatField(default=0.0),
        ),
        migrations.DeleteModel(
            name='Position',
        ),
    ]