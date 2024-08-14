from django.db import models
from django.contrib.auth.models import AbstractUser


class Group(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=2000)

    def __str__(self):
        return self.name


class Level(models.Model):
    level = models.CharField(max_length=300)

    def __str__(self):
        return self.level


class Course(models.Model):
    creator = models.ForeignKey('User', on_delete=models.SET("Unknown Creator"))
    picture = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.SET("Unknown Group"))
    format = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    level = models.ManyToManyField(Level, related_name='courses', blank=True)
    description = models.TextField(max_length=1000)
    file = models.FileField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', 'name']

    def __str__(self):
        return f"{self.name} _ {self.group}"


class User(AbstractUser):
    courses = models.ManyToManyField(Course, related_name='users', blank=True)
    avatar = models.ImageField(null=True, default='avatar.svg')
    bio = models.TextField(null=True)


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body



