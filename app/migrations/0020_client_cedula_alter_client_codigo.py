# Generated by Django 4.1.3 on 2023-06-30 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_client_codigo_alter_paciente_peso'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='cedula',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='codigo',
            field=models.CharField(default='TJHJSUB', editable=False, max_length=7, null=True),
        ),
    ]