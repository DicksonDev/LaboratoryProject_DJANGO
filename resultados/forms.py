from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import MedicalResult
from .models import TipoExamen
import re

User = get_user_model()  # Obtiene el modelo de usuario actual es decir, CustomUser


# Formulario personalizado para crear un nuevo usuario
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
    widgets = {
        'first_name': forms.TextInput(attrs={
            'placeholder': 'Nombre',
            'class': 'form-control'
        }),
        'last_name': forms.TextInput(attrs={
            'placeholder': 'Apellido',
            'class': 'form-control'
        }),
        'email': forms.EmailInput(attrs={
            'placeholder': 'Correo electrónico',
            'class': 'form-control'
        }),
        'password1': forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control'
        }),
        'password2': forms.PasswordInput(attrs={
            'placeholder': 'Confirmar contraseña',
            'class': 'form-control'
        }),
    }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        # Validar contraseña: mínimo 8 caracteres, letras y números (puedes ajustar regex)
        if len(password) < 8:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'\d', password):
            raise forms.ValidationError(
                "La contraseña debe contener al menos un número.")
        if not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError(
                "La contraseña debe contener al menos una letra.")
        return password

    class Meta:
        model = User  # Ahora usa el modelo `CustomUser`
        fields = ('first_name', 'last_name', 'email', 'password1',
                  'password2')  # Campos que se mostrarán en el formulario


class CustomUserEditWithPasswordForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Nueva Contraseña",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_staff']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        user_id = self.instance.id
        if User.objects.exclude(pk=user_id).filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
            if len(password1) < 8:
                raise forms.ValidationError(
                    "La contraseña debe tener al menos 8 caracteres.")

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user


class MedicalResultForm(forms.ModelForm):
    class Meta:
        model = MedicalResult
        fields = ['user', 'tipoExamen', 'examen_Image', 'observaciones']
        labels = {
            'user': 'Correo',
            'tipoExamen': 'Tipo de examen',
            'examen_Image': 'Examen imagen',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'tipoExamen': forms.Select(attrs={'class': 'form-select'}),
            'examen_Image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe observaciones aquí...'
            }),
        }

    def clean_examen_Image(self):
        image = self.cleaned_data.get('examen_Image')
        if not image:
            raise forms.ValidationError("Debes subir una imagen del examen.")
        return image

    def clean_user(self):
        user = self.cleaned_data.get('user')
        if not user:
            raise forms.ValidationError("Debes seleccionar un usuario.")
        return user


class TipoExamenForm(forms.ModelForm):

    class Meta:
        model = TipoExamen
        fields = ['nombre', 'descripcion']
        labels = {
            'nombre': 'Nombre del examen',
            'descripcion': 'Descripción (opcional)',
        }
        help_texts = {
            'nombre': 'Escribe el nombre único del tipo de examen.',
            'descripcion': 'Puedes agregar detalles o aclaraciones sobre este examen.',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Hematología'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej. Examen de sangre para evaluar glóbulos rojos...'
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if TipoExamen.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Este tipo de examen ya existe.")
        return nombre
