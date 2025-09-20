from django.shortcuts import redirect
from django.urls import path , include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/login/',auth_views.LoginView.as_view(template_name="registration/login.html",redirect_authenticated_user=True),name='login'),
    path('accounts/signup/', views.UserCreateView.as_view() , name="signup"),
    path('courses/', views.CourseListView.as_view() , name="courses"),
    path('courses/create/', views.CourseCreateView.as_view() , name="course-create"),
    path('courses/<slug>/update/', views.CourseUpdateView.as_view() , name="course-update"),
    path('courses/<slug>/delete/', views.CourseDeleteView.as_view() , name="course-delete"),
    path('courses/<slug>', views.CourseDetailView.as_view() , name="course-detail"),
    path('courses/<pk>/documents/', views.DocumentDetailView.as_view() , name="document-detail"),
    path('courses/<slug>/documents/new/', views.DocumentCreateView.as_view() , name="document-create"),
    path('documents/<int:pk>/update-doc/', views.DocumentUpdateView.as_view() , name="document-update"),
    path('documents/<int:pk>/delete-doc/', views.DocumentDeleteView.as_view() , name="document-delete"),
    path('documents/<int:pk>/flashcard/create/', views.FlashcardCreateView.as_view() , name="flashcard-create"),
    path('documents/<int:pk>/flashcard/delete/', views.FlashcardDeleteView.as_view() , name="flashcard-delete"),
    path('documents/<int:pk>/flashcard/update/', views.FlashcardUpdateView.as_view() , name="flashcard-update"),
    path('documents/<int:pk>/flashcard/generate/', views.FlashcardGenerate.as_view() , name="flashcard-generate"),
    path('', views.LandingPageView.as_view() , name="home"),
]
