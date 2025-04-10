# Generated by Django 4.2.10 on 2025-04-01 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_stand_analysis_stand_location_stand_location_index1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stand_analysis',
            name='sa_analysis_boolean',
        ),
        migrations.RemoveField(
            model_name='stand_analysis',
            name='sa_analysis_description',
        ),
        migrations.RemoveField(
            model_name='stand_analysis',
            name='sa_analysis_float',
        ),
        migrations.RemoveField(
            model_name='stand_analysis',
            name='sa_analysis_integer',
        ),
        migrations.RemoveField(
            model_name='stand_analysis',
            name='sa_analysis_string',
        ),
        migrations.AddField(
            model_name='stand_analysis',
            name='sa_analysis_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='analysis type'),
        ),
        migrations.AddField(
            model_name='stand_analysis',
            name='sa_analysis_value',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='analysis value'),
        ),
    ]
