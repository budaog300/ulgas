# Generated by Django 4.2.6 on 2023-12-25 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avtoriz', '0012_deviceaccount_dateend'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreement',
            name='idDogovor',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
