# Generated by Django 4.2.7 on 2024-02-04 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_lessonpage_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
