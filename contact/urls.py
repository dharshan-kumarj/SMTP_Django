from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.contact_form, name='contact_form'),
]
