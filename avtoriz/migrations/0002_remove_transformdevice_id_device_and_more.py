# Generated by Django 4.2.6 on 2023-12-04 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avtoriz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transformdevice',
            name='id_device',
        ),
        migrations.DeleteModel(
            name='UserTransformator',
        ),
        migrations.DeleteModel(
            name='TransformDevice',
        ),
    ]