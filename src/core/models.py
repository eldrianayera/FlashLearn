from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course_note = models.TextField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name


class Document(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    document_note = models.TextField(max_length=50, blank=True)
    summary = models.TextField(max_length=50, null=True, blank=True)
    course = models.ForeignKey(Course, related_name='documents', on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/', null=True)
    
    def __str__(self):
        return self.name

class Flashcard(models.Model):
    question = models.CharField(max_length=50)
    answer = models.CharField(max_length=100)
    document = models.ForeignKey(Document, related_name='flashcards', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.question

