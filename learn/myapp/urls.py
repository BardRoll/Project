from myapp import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('about', views.about),
    path('form', views.form),
    path('edit/<person_id>', views.edit),
    path('delete/<person_id>', views.delete),
]
