# Generated by Django 4.2.10 on 2025-04-04 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_rename_pricing_rules_base_pricing_rules'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricing_rules',
            name='prb_quantity',
            field=models.IntegerField(blank=True, null=True, verbose_name='pricing rule base quantity'),
        ),
    ]
