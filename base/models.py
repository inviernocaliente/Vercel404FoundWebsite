from django.db import models
from django.contrib.auth.models import AbstractUser
from django.views.generic.detail import DetailView



class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique = True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

#----------------------------------------- Course Models ----------------------------------------------#

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    #is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class LessonPage(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_pages')
    title = models.CharField(max_length=200)
    content = models.TextField(default="Default lesson content")
    google_slide_embed_url = models.URLField(blank=True, null=True)
    python_compiler_embed_url = models.URLField(blank=True, null=True)
    replit_embed_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title 

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    lesson_page = models.ForeignKey(LessonPage, on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    entered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson_page')

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.lesson_page.title}"
        return f"Anonymous - {self.lesson_page.title}"

class UserLessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    entered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.title}"
        return f"Anonymous - {self.lesson.title}"
