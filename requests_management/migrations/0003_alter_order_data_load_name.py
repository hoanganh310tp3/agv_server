# Generated by Django 5.0.3 on 2024-11-14 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests_management', '0002_remove_order_data_is_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_data',
            name='load_name',
            field=models.CharField(default='none', max_length=16),
        ),
    ]
