# Generated by Django 5.0.6 on 2025-01-02 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_name', models.CharField(max_length=20)),
                ('tax_percentage', models.FloatField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
