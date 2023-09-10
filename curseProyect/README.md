# Nombre del Proyecto

Bienvenido a Eventix, una plataforma versátil y completa diseñada para simplificar la planificación, gestión y ejecución de eventos de todo tipo. Nuestra aplicación proporciona a organizadores de eventos, y asistentes las herramientas necesarias para crear y disfrutar de experiencias memorables. Desde la creación de eventos personalizados hasta la gestión de invitados y la colaboración con organizadores.

¡Comienza a utilizar [Nombre del Proyecto] hoy mismo y descubre cómo podemos transformar tus eventos en momentos inolvidables!
## Requisitos Previos

- Python >3.8: [Descargar Python](https://www.python.org/downloads/)
- pip: El gestor de paquetes de Python. Normalmente se instala junto con Python.
- Virtualenv (recomendado)


### 1. Clonar el Repositorio

Primero, clona este repositorio en tu máquina local:

```bash
git clone https://github.com/sebas230704/Integrative-project.git

```

## 2. Virtualenv and django

Una vez este abierto el proyecto abre una consola (lo puedes hacer en la consola de VS code en caso de que lo prefieras) y ubicate
en la direccion de la carpeta del proyecto "\curseProyect" (donde esta este archivo: README.md) y ejecuta los siguientes comandos

- pip install virtualenv  (recomendado)
- virtualenv venv
- .\venv\Scripts\activate   (activamos el entorno virtual siempre que vayamos a trabajar en el proyecto y realizar cualquier cambio e instalaciones)
   cuando actives el entorno virtual fijate que te quede algo asi: "(venv) PS C:\RUTA\RUTA\RUTA\ETC"

- pip install django
- pip install mysqlclient      (instalamos mysqlclient para trabajar con mysql antes de correr el servidor)
- python manage.py runserver   (ahora, si deseas, puedes ejecutar el proyecto para verificar que todo este correcto)


## 3. Actualizar cambios en el gestor de BD mysql

en la misma carpeta "\curseProyect"  ejecuta

 Al momento de realizar algun cambio ejecuta siempre para actualizar la base de datos:

 - python manage.py makemigrations
 - python manage.py migrate

Ahora en settings.py debes actualizar esta configuración para que coincida con MySQL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nombre_de_tu_base_de_datos',
        'USER': 'tu_usuario_de_mysql',
        'PASSWORD': 'tu_contraseña_de_mysql',
        'HOST': 'localhost',  # Puede variar según la configuración de tu servidor MySQL
        'PORT': '',           # Deja en blanco para usar el puerto predeterminado
    }
}


## 3. Empezar Entorno de Desarrollo

Una vez tengas el entorno virtual installado y django ejecuta dentro de la :

- python manage.py runserver (ingresar al enlace para emepzar el servidor: ejemplo: http://127.0.0.1:8000)

 
## Licencia

Este proyecto está bajo la Licencia [Nombre de la Licencia]. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.

## Contacto

- Nombre del Autor: 
- Correo Electrónico:
- Enlace a tu sitio web o perfil en GitHub: 


