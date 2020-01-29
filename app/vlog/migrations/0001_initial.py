# Generated by Django 3.0.2 on 2020-01-29 15:35

import contrib.timescale.fields
from django.db import migrations, models
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VlogRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('time', contrib.timescale.fields.TimescaleDateTimeField(default=django.utils.timezone.now, interval='1 week')),
                ('vri_id', models.IntegerField()),
                ('message_type', models.PositiveSmallIntegerField()),
                ('message', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddConstraint(
            model_name='vlogrecord',
            constraint=models.UniqueConstraint(fields=('vri_id', 'time'), name='vri_time'),
        ),
    ]
