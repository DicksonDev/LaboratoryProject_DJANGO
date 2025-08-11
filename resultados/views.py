from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from .forms import CustomUserForm
from .forms import MedicalResultForm
from .forms import TipoExamenForm
from .forms import CustomUserEditWithPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import MedicalResult
from .models import TipoExamen
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from fpdf import FPDF
import os
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.views import PasswordResetView

User = get_user_model()  # Obtiene el modelo de usuario actual


def inicio(request):  # Vista de inicio
    return render(request, 'index.html')


def register(request):  # Vista de registro
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            enviar_correo_bienvenida(user)
            return redirect('login')
    else:
        form = CustomUserForm()

    # Volver a renderizar la página con los errores visibles
    return render(request, 'register.html', {'form': form})


def signin(request):  # Vista de inicio de sesión

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




@login_required
def bienvenido(request):  # Vista de bienvenida
    resultados = MedicalResult.objects.filter(
        user=request.user, eliminado=False)
    return render(request, 'cliente_vista.html', {'resultados': resultados})


@login_required
def perfil(request):
    user = request.user
    # Contar exámenes del usuario (excluyendo eliminados si quieres)
    total_examenes = MedicalResult.objects.filter(user=user, eliminado=False).count()

    context = {
        'user': user,
        'total_examenes': total_examenes,
    }
    return render(request, 'perfil.html', context)

@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Cierra sesión antes de eliminar
        user.delete()    # Elimina el usuario
        messages.success(request, 'Tu cuenta ha sido eliminada.')
        return redirect('inicio')  # Cambia 'home' por la url de tu página principal
    else:
        return redirect('perfil')


def signout(request):  # Vista de cierre de sesión
    logout(request)
    return redirect('inicio')


def es_admin(user):  # Verifica si el usuario es administrador
    return user.is_authenticated and user.is_staff


def enviar_correo_bienvenida(usuario):
    asunto = "Bienvenido a Divina Misericordia"
    from_email = "laboratoriodivinamisericordia2@gmail.com"
    to = usuario.email

    contexto = {
        "nombre": usuario.first_name,
        "logo_url": "{% static 'app2/images/logo.png' %}",
    }

    html_content = render_to_string("correo_bienvenida.html", contexto)
    text_content = f"Hola {usuario.first_name}, gracias por registrarte en nuestro sistema."

    msg = EmailMultiAlternatives(asunto, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'  # Tu template HTML
    subject_template_name = 'registration/password_reset_subject.txt'  # Un template para el asunto, sólo texto plano

    def form_valid(self, form):
        """
        Cuando el formulario es válido, enviamos el email con HTML adjunto.
        """
        opts = {
            'use_https': self.request.is_secure(),
            'from_email': None,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.email_template_name,
        }
        # El método send_mail envía el correo
        form.save(**opts)
        return super().form_valid(form)




def servicios(request):  # Vista de servicios
    return render(request, 'servicios.html')


@login_required
def eliminar_examen(request, pk):  # Endpoint para eliminar un examen desde el cliente
    examen = get_object_or_404(MedicalResult, pk=pk, user=request.user)
    examen.eliminado = True
    examen.save()
    return redirect('bienvenido')


@login_required
@user_passes_test(es_admin)
def listar_usuarios(request):
    query = request.GET.get("q", "").strip()

    if query:
        usuarios = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        usuarios = User.objects.all()

    # Ordenar para que la paginación sea consistente
    usuarios = usuarios.order_by("first_name", "last_name")

    # PAGINACIÓN: 10 usuarios por página
    paginator = Paginator(usuarios, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "listar_usuarios.html",
        {"page_obj": page_obj, "query": query}
    )


@login_required
@user_passes_test(es_admin)
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            enviar_correo_bienvenida(user)
            messages.success(request, "Usuario creado exitosamente.")
            return redirect('crear_usuario')
        else:
            messages.error(request, "Por favor corrige los errores.")
    else:
        form = CustomUserForm()
    return render(request, 'crear_usuario.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def editar_usuario(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserEditWithPasswordForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data.get("password1")
            if new_password:
                user.set_password(new_password)
            user.save()
            messages.success(request, "Usuario actualizado exitosamente.")
            return redirect('listar_usuarios')
        else:
            messages.error(request, "Corrige los errores.")
    else:
        form = CustomUserEditWithPasswordForm(instance=user)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario': user})


@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect('listar_usuarios')


@login_required
@user_passes_test(es_admin)
def listar_examenes(request):
    query = request.GET.get('q', '').strip()

    # Solo mostrar los examenes que no están eliminados
    examenes = MedicalResult.objects.filter(eliminado=False)

    if query:
        examenes = examenes.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__email__icontains=query) |
            Q(tipoExamen__nombre__icontains=query) |
            Q(fecha__icontains=query)
        )

    return render(request, 'listar_examenes.html', {
        'examenes': examenes,
        'query': query
    })


@login_required
@user_passes_test(es_admin)
def crear_examen(request):
    if request.method == 'POST':
        form = MedicalResultForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Examen médico creado exitosamente.")
            return redirect('crear_examen')
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = MedicalResultForm()
    return render(request, 'crear_examen.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def editar_examen(request, id):
    examen = get_object_or_404(MedicalResult, id=id)

    if request.method == 'POST':
        form = MedicalResultForm(request.POST, request.FILES, instance=examen)
        if form.is_valid():
            form.save()
            return redirect('listar_examenes')
    else:
        form = MedicalResultForm(instance=examen)

    return render(request, 'editar_examen.html', {'form': form, 'examen': examen})


@login_required
@user_passes_test(es_admin)
# Endpoint para eliminar un examen de forma permanente desde el administrador
def eliminar_examen_permanente(request, id):
    examen = get_object_or_404(MedicalResult, id=id)
    examen.delete()
    return redirect('listar_examenes')


@login_required
@user_passes_test(es_admin)
def listar_tipos_examen(request):
    tipos = TipoExamen.objects.all()
    return render(request, 'listar_tipo_de_examen.html', {'tipos': tipos})


@login_required
@user_passes_test(es_admin)
def crear_tipo_examen(request):
    if request.method == 'POST':
        form = TipoExamenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de examen creado exitosamente.")
            return redirect('crear_tipo_examen')
        else:
            messages.error(
                request, "Por favor corrige los errores en el formulario.")
    else:
        form = TipoExamenForm()

    return render(request, 'crear_tipo_examen.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def editar_tipo_de_examen(request, id):
    tipo = get_object_or_404(TipoExamen, id=id)
    if request.method == 'POST':
        form = TipoExamenForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('listar_tipos_examen')
    else:
        form = TipoExamenForm(instance=tipo)
    return render(request, 'editar_tipo_de_examen.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def eliminar_tipo_de_examen(request, id):
    tipo = get_object_or_404(TipoExamen, id=id)
    tipo.delete()
    return redirect('listar_tipos_examen')


class PDF(FPDF):
    def header(self):
        self.image('resultados/static/app2/images/logo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.multi_cell(
            0, 10, 'Reporte Mensual de Examenes Enviados', align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')


@login_required
@user_passes_test(es_admin)
def generar_reporte_mensual_pdf(request):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    hoy = timezone.now()
    mes_actual = hoy.month
    anio_actual = hoy.year

    examenes = MedicalResult.objects.filter(
        fecha__month=mes_actual,
        fecha__year=anio_actual
    )

    pdf.cell(40, 10, 'Paciente', 1)
    pdf.cell(50, 10, 'Examen', 1)
    pdf.cell(40, 10, 'Fecha', 1)
    pdf.cell(60, 10, 'Observaciones', 1)
    pdf.ln()

    for ex in examenes:
        nombre = ex.user.get_full_name() if ex.user else 'N/A'
        tipo = ex.tipoExamen.nombre
        fecha = ex.fecha.strftime('%d/%m/%Y')
        observ = ex.observaciones if ex.observaciones else ''

        pdf.cell(40, 10, nombre, 1)
        pdf.cell(50, 10, tipo, 1)
        pdf.cell(40, 10, fecha, 1)
        pdf.cell(60, 10, observ, 1)
        pdf.ln()

    # Guardar el PDF en un objeto BytesIO para evitar problemas con output
    from io import BytesIO
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{mes_actual}_{anio_actual}.pdf"'

    return response
