from email.policy import default

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models. CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models. TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

        def __str__(self):
            return self.name


class Question(models.Model):
    text = models.TextField()
    category = models.ForeignKey(Category, no_delete=models. CASCADE, related_name='questions')
    time_limit = models.IntegerField(default=30)
    points = models.IntegerField(default=30)
    order = models.IntegerField(default=10)

    def __str__(self):
        return self.text[:50]

class Answer(models.Model):
    question = models.ForeignKey(Question ,on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:50]

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    score =models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    time_taken = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total_questions}"

