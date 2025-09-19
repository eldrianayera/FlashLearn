from django.urls import path , include
from . import views

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/signup/', views.UserCreateView.as_view() , name="signup"),
    path('courses/', views.CourseListView.as_view() , name="courses"),
    path('courses/create/', views.CourseCreateView.as_view() , name="course-create"),
    path('courses/<slug>/update/', views.CourseUpdateView.as_view() , name="course-update"),
    path('courses/<slug>/delete/', views.CourseDeleteView.as_view() , name="course-delete"),
    path('courses/<slug>', views.CourseDetailView.as_view() , name="course-detail"),
    path('courses/<slug>/documents/new/', views.DocumentCreateView.as_view() , name="document-create"),
    path('documents/<int:pk>/update-doc/', views.DocumentUpdateView.as_view() , name="document-update"),
    path('documents/<int:pk>/delete-doc/', views.DocumentDeleteView.as_view() , name="document-delete"),
    path('', views.LandingPageView.as_view() , name="home"),
]
