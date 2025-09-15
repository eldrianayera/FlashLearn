from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('documents', views.DocumentViewSet)
router.register('courses', views.CourseViewSet)
router.register('flashcards', views.FlashcardViewSet)

urlpatterns = [
    path('',include(router.urls))
]
