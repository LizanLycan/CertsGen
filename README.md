# Instrucciones de instalación

## Para información de deployment:

Veáse las posibilidades disponibles en [Django deployment docs](https://docs.djangoproject.com/en/3.0/howto/deployment/)

## Para instalación de paquetes y base de datos

### Instalar paquetes

1. Garantizar instalación de `pip` y demas dependencias de Django. Asi como del entorno frontend, `npm` y demas.
2. Configurar el entorno virtual con `venv`.
3. Iniciar entorno virtual
4. Correr en root `pip install -r requirements.txt`
5. Instalar frontend en root `npm install`

### Preparar migraciones y data en base de datos

Correr:

`python manage.py migrate`.

`python manage.py loaddata initial_data`.

### Servir Frontend

Solo se deben generar estaticos, correr en root `npm run build`
