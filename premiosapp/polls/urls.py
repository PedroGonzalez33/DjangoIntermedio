from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),

    path("detail/<int:question_id>", views.DetailView.as_view(), name="detail"),

    path("results/<int:question_id>", views.ResultView.as_view(), name="results"),

    path("vote/<int:question_id>", views.vote, name="vote"),

]