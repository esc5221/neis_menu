from django.urls import path, include
from rest_framework.routers import SimpleRouter
from menus.views import MenuView, MenuWeeklyView

app_name = "menus"

urlpatterns = [
    path("schools/<int:school_id>/menus/", MenuView.as_view()),
    path("schools/<int:school_id>/menus/weekly/", MenuWeeklyView.as_view()),
]
