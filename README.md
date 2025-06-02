# 🧪 LaboratoryProject_DJANGO

Este proyecto es una aplicación web desarrollada con Django que permite al laboratorio clínico "Divina Misericorida" gestionar usuarios y exámenes médicos. Los pacientes pueden iniciar sesión para ver sus propios resultados (como imágenes), mientras que los administradores pueden subir exámenes desde el panel de administración.

---

## 📚 Tabla de Contenidos

- [🛠️ Tecnologías](#-tecnologías)
- [🚀 Instalación](#-instalación)
- [👥 Uso](#-uso)
- [🧪 Características Clave](#-características-clave)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [📄 Licencia](#-licencia)
- [👨‍💻 Autor](#-autor)

---

## 🛠️ Tecnologías

- asgiref v3.8.1
- dj-database-url v2.3.0
- Django v5.2
- gunicorn v23.0.0
- packaging v25.0
- pillow v11.2.1
- python-decouple v3.8
- sqlparse v0.5.3
- typing_extensions v4.13.2
- tzdata v2025.2
- whitenoise v6.9.0

---

## 🚀 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/DicksonDev/LaboratoryProject_DJANGO.git
   cd LaboratoryProject_DJANGO
   ```

2. Crea y activa un entorno virtual:

   - **Linux/macOS:**
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```
   - **Windows:**
     ```bash
     python -m venv env
     env\Scripts\activate
     ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Aplica las migraciones:

   ```bash
   python manage.py migrate
   ```
  ---

## 👥 Uso

1. Crea un superusuario para acceder al panel de administración y gestionar usuarios como examenes medicos:

   ```bash
   python manage.py createsuperuser
   ```

2. Inicia el servidor local:

   ```bash
   python manage.py runserver
   ```

3. Accede al panel de administración en:  
   http://127.0.0.1:8000/admin/

4. Desde el panel:
   - Crea usuarios con rol de paciente.
   - Sube exámenes clínicos (imágenes u otros archivos) asociados a cada paciente.

5. Los pacientes pueden iniciar sesión desde la interfaz pública y ver **solo sus propios exámenes**.

---

## 🧪 Características Clave

- ✔️ Registro y autenticación de usuarios (pacientes).
- ✔️ Panel de administración para gestión de usuarios y exámenes.
- ✔️ Subida de exámenes médicos con archivos/imágenes.
- ✔️ Los pacientes solo pueden ver sus propios resultados.
- ✔️ Protección de rutas según roles (admin / paciente).
- ✔️ Interfaz web sencilla y funcional.

---

## 📁 Estructura del Proyecto

```
LaboratoryProject_DJANGO/
├── laboratorio/                  # Configuración principal del proyecto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── resultados/                   # Aplicación principal que maneja los resultados clínicos
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── static/
│   ├── templates/
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── media/                        # Archivos subidos por los usuarios
├── .gitignore
├── manage.py
└── requirements.txt
```
## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

---

## 👨‍💻 Autor

Desarrollado por [DicksonDev](https://github.com/DicksonDev) como parte de un proyecto académico del segundo año de Ingeniería Informática.

---
