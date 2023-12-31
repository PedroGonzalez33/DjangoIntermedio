from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),

    path("detail/<int:pk>", views.DetailView.as_view(), name="detail"),

    path("results/<int:pk>", views.ResultView.as_view(), name="results"),

    path("vote/<int:pk>", views.vote, name="vote"),

]