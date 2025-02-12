# Generated by Django 5.0.6 on 2025-01-18 02:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_orderitemstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='service_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orderitem', to='service.services'),
        ),
    ]
