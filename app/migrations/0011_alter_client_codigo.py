# Generated by Django 4.1.3 on 2022-11-26 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_esta_pagada_citas_activa_alter_client_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='codigo',
            field=models.CharField(default='ZBSZALQ', editable=False, max_length=7, null=True),
        ),
    ]
