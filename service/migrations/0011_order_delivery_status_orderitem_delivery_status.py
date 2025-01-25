# Generated by Django 5.0.6 on 2025-01-25 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0010_invoicecounter_invoicecounter_singleton_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('Not Delivered', 'Not Delivered'), ('Partially Delivered', 'Partially Delivered'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Not Delivered', max_length=30),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='delivery_status',
            field=models.CharField(choices=[('Not Delivered', 'Not Delivered'), ('Partially Delivered', 'Partially Delivered'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Not Delivered', max_length=30),
        ),
    ]
