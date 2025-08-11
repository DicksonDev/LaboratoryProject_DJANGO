from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView

# Nuestras url's
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.signin, name='login'),
    path('register/', views.register, name='register'),
    path('bienvenido/', views.bienvenido, name='bienvenido'),
    path('servicios/', views.servicios, name='servicios'),
    path('eliminar-examen/<int:pk>/',
         views.eliminar_examen, name='eliminar_examen'),
    path('logout/', views.signout, name='logout'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/',
         views.eliminar_usuario, name='eliminar_usuario'),
    path('examenes/', views.listar_examenes, name='listar_examenes'),
    path('crear-examen/', views.crear_examen, name='crear_examen'),
    path('editar_examen/<int:id>/', views.editar_examen, name='editar_examen'),
    path('eliminar_examen/<int:id>/',
         views.eliminar_examen_permanente, name='eliminar_examen_permanente'),
    path('listar_tipos_examen/', views.listar_tipos_examen,
         name='listar_tipos_examen'),
    path('crear-tipo-examen/', views.crear_tipo_examen, name='crear_tipo_examen'),
    path('editar_tipo_examen/<int:id>/',
         views.editar_tipo_de_examen, name='editar_tipo_de_examen'),
    path('eliminar_tipo_examen/<int:id>/',
         views.eliminar_tipo_de_examen, name='eliminar_tipo_de_examen'),
    path('reporte-mensual/', views.generar_reporte_mensual_pdf,
         name='generar_reporte_mensual_pdf'),
    path('miperfil/', views.perfil, name='perfil'),
    path('eliminar_cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
