from django.urls import path

from . import views

app_name = 'matrix'
urlpatterns = [
    path('', views.index, name='index'),
]
