# Generated by Django 5.0.6 on 2025-01-02 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('authority', models.CharField(blank=True, help_text='Authorities that regulate the service (eg: MCA, FAIC etc)', max_length=100, null=True)),
                ('price', models.FloatField()),
                ('price_before_tax', models.FloatField(blank=True, default=0, null=True)),
                ('tax_amount', models.FloatField(default=0)),
                ('tax', models.CharField(choices=[('Inclusive', 'Inclusive'), ('Exclusive', 'Exclusive')], default='Inclusive', max_length=20)),
                ('tax_value', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.tax')),
            ],
        ),
    ]
