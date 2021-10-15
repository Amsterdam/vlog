# Generated by Django 3.2.8 on 2021-10-15 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reistijden_v1', '0011_02_measurement_sites'),
    ]

    operations = [
        migrations.AddField(
            model_name='trafficflowcategorycount',
            name='vehicle_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reistijden_v1.vehiclecategory'),
        ),
        migrations.AlterField(
            model_name='trafficflowcategorycount',
            name='type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
