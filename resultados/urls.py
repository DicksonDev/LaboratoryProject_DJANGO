from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.signin, name='login'),
    path('register/', views.register, name='register'),
    path('bienvenido/', views.bienvenido, name='bienvenido'),
    path('logout/', views.signout, name='logout'),
    path('eliminar-examen/<int:pk>/',
         views.eliminar_examen, name='eliminar_examen'),
]
