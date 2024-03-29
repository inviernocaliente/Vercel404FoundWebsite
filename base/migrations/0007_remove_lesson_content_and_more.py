# Generated by Django 4.2.7 on 2024-01-21 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_userprogress_remove_lesson_lessonreferencenumber_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='content',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='google_slide_embed_url',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='python_compiler_embed_url',
        ),
        migrations.AddField(
            model_name='lesson',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='LessonPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField(default='Default lesson content')),
                ('google_slide_embed_url', models.URLField(blank=True, null=True)),
                ('python_compiler_embed_url', models.URLField(blank=True, null=True)),
                ('replit_embed_url', models.URLField(blank=True, null=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.lesson')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userprogress',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='userprogress',
            name='lessonpage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.lessonpage'),
        ),
        migrations.AlterUniqueTogether(
            name='userprogress',
            unique_together={('user', 'lessonpage')},
        ),
        migrations.RemoveField(
            model_name='userprogress',
            name='lesson',
        ),
    ]
