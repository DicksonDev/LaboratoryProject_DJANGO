from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()  # Obtiene el modelo de usuario actual


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label="Nombre", widget=forms.TextInput(
        attrs={'placeholder': 'Nombre'}))
    last_name = forms.CharField(max_length=100, label="Apellido", widget=forms.TextInput(
        attrs={'placeholder': 'Apellido'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Correo electrónico'}))
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        help_text="Debe tener al menos 8 caracteres y ser segura."
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirmar contraseña'}),
        help_text="Repite la contraseña."
    )

    class Meta:
        model = User  # Ahora usa el modelo `CustomUser`
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
