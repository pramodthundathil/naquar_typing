# Generated by Django 5.0.6 on 2025-01-03 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='govt_fee',
            field=models.FloatField(default=0, help_text='Government fee for the service'),
        ),
        migrations.AddField(
            model_name='services',
            name='total_fund_from_customer',
            field=models.FloatField(default=0, help_text='Total amount collected from customer including govt fee'),
        ),
        migrations.AlterField(
            model_name='services',
            name='price',
            field=models.FloatField(default=0, help_text='Price of the service after deducting govt fee'),
        ),
    ]
