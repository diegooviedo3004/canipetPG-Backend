# Generated by Django 4.1.3 on 2023-06-30 03:03

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_client_codigo_alter_product_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='codigo',
            field=models.CharField(default='FX3RDER', editable=False, max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='peso',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[app.models.non_negative_validator]),
        ),
    ]
