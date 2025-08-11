from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TipoExamen, MedicalResult

# Personalización del UserAdmin


@admin.register(CustomUser)  # Registramos el modelo CustomUser en el admin
# Hacemos un CustomUserAdmin que hereda de UserAdmin ya que eliminamos campo username
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    # Como eliminamos username, tenemos que ajustar los campos que se muestran
    fieldsets = (  # Edicion de usuario
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
        ('Permisos', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (  # Creacion de usuario
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

# Admin para TipoExamen


@admin.register(TipoExamen)
class TipoExamenAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# Admin para MedicalResult


@admin.register(MedicalResult)
class MedicalResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipoExamen', 'fecha')
    list_filter = ('tipoExamen', 'fecha')
    search_fields = ('user__email', 'tipoExamen__nombre')
    # facilita la búsqueda de usuarios/exámenes
    autocomplete_fields = ['user', 'tipoExamen']


# Perzonalicacion del panel administrativo
admin.site.site_header = "Administración Divina Misericordia"
admin.site.site_title = "Divina Misericordia Admin"
admin.site.index_title = "Bienvenido al Panel de Administración"
