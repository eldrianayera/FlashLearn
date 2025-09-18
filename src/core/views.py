from django.shortcuts import render
from rest_framework import viewsets
from .models import Course , User , Document , Flashcard
from .serializers import CourseSerializer , UserSerializer , DocumentSerializer , FlashcardSerializer
from rest_framework.permissions import IsAuthenticated

from core import serializers


# Create your views here.

class UserFilteredViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseViewSet(UserFilteredViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class DocumentViewSet(UserFilteredViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FlashcardViewSet(UserFilteredViewSet):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer