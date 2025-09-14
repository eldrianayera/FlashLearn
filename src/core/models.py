from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Course(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course_note = models.TextField(max_length=50)


class Document(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    document_note = models.TextField(max_length=50)
    summary = models.TextField(max_length=50, null=True)
    course = models.ForeignKey(Course, related_name='documents', on_delete=models.CASCADE)

class Flashcard(models.Model):
    question = models.CharField(max_length=50)
    answer = models.CharField(max_length=100)
    document = models.ForeignKey(Document, related_name='flashcards', on_delete=models.CASCADE)

