# Generated by Django 4.2.6 on 2023-12-15 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avtoriz', '0007_alter_agreement_number_agreement'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceaccount',
            name='meter_interval',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='deviceaccount',
            name='tr_k',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
