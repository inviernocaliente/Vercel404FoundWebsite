# Generated by Django 4.2.7 on 2024-01-26 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_rename_lessonpage_userprogress_lesson_page_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonpage',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
