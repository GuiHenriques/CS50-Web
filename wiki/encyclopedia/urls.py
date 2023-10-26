from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("edit", views.edit, name="edit"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random"),
    path("<str:name>", views.entry, name="entry"),
]
