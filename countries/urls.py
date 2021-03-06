from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<keyword>/', views.search),
    path('detail/<keyword>/', views.detail),
]
