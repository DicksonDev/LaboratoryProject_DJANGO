from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# UserManager personalizado (eliminamos username y usamos email como identificador único)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Modelo de usuario personalizado


class CustomUser(AbstractUser):
    username = None  # Eliminamos el campo de username
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()  # Usamos el UserManager personalizado

    def __str__(self):
        return self.email

# Tipo de examen


class TipoExamen(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre}"

# Resultados médicos


class MedicalResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tipoExamen = models.ForeignKey(TipoExamen, on_delete=models.CASCADE)
    examen_Image = models.ImageField(
        upload_to='examenes/', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    eliminado = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipoExamen.nombre} - {self.user.email}"  # pylint: disable=no-member
