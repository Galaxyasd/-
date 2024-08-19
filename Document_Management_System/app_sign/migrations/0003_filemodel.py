# Generated by Django 5.1 on 2024-08-16 09:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_sign', '0002_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('size', models.IntegerField()),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('attributes', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
