# Generated by Django 4.2.6 on 2023-12-04 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avtoriz', '0005_alter_accountpoint_conclusion_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='id_Ulges',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='id_Ulges',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
