# Generated by Django 4.2.6 on 2024-01-22 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avtoriz', '0014_usernote'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Обращения',
                'verbose_name_plural': 'Обращения пользователей',
            },
        ),
    ]