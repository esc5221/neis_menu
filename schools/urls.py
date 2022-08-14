from django.urls import path, include
from rest_framework.routers import SimpleRouter
from schools.views import SchoolListCreateView, SchoolView

app_name = 'schools'

urlpatterns = [
    path('schools/<int:pk>/', SchoolView.as_view()),
    path('schools/', SchoolListCreateView.as_view()),
]