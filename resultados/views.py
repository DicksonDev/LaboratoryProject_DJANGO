from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import MedicalResult
from django.shortcuts import get_object_or_404


def inicio(request):
    return render(request, 'index.html')


User = get_user_model()  # Obtiene el modelo de usuario actual


def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            # Redirigir al login si el registro es exitoso
            return redirect('login')
    else:
        form = CustomUserForm()

    # Volver a renderizar la página con los errores visibles
    return render(request, 'register.html', {'form': form})


@login_required
def bienvenido(request):
    resultados = MedicalResult.objects.filter(
        user=request.user, eliminado=False)
    return render(request, 'cliente_vista.html', {'resultados': resultados})


@login_required
def eliminar_examen(request, pk):
    examen = get_object_or_404(MedicalResult, pk=pk, user=request.user)
    examen.eliminado = True
    examen.save()
    return redirect('bienvenido')


def signin(request):
    storage = messages.get_messages(request)
    storage.used = True  # Limpia mensajes

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            try:
                # Buscar usuario por email
                user = User.objects.get(email=email)
                # Autenticar con su username
                user = authenticate(
                    request, username=email, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                return redirect("bienvenido")
            else:
                messages.error(request, "Correo o contraseña incorrectos.")
        else:
            messages.error(request, "Error en el formulario.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def signout(request):
    logout(request)
    return redirect('inicio')
