# Generated by Django 4.2.6 on 2023-12-18 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avtoriz', '0009_objectaccount_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objectaccount',
            name='is_active',
            field=models.CharField(max_length=2, null=True),
        ),
    ]