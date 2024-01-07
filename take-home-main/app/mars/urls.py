from django.urls import path
from . import views

urlpatterns = [
    path('', views.mars_index)
]
