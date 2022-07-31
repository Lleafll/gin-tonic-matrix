from django.urls import path

from . import views

app_name = "matrix"
urlpatterns = [
    path("", views.index, name="index"),
    path(
        "<int:gin_id>/<int:tonic_id>/",
        views.evaluations,
        name="evaluations"),
    path(
        "<int:gin_id>/<int:tonic_id>/evaluate",
        views.evaluate,
        name="evaluate")
]
