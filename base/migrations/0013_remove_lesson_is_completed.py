# Generated by Django 4.2.7 on 2024-02-04 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_userlessonprogress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='is_completed',
        ),
    ]
