# MicroServicio Cuentas de Usuario

## Microservicio hecho por:
* Alejandro Zambrano
* Laura Murillas 

## Funcionalidad
En este microservicio se gestiona el backend y en frontend donde el usuario podrá:
* Iniciar sesión
* Crear una cuenta
* Salir de la cuenta
* Activacion de la cuenta via correo electronico
* Modificar los datos de la cuenta

## Requisitos para ejecutar el proyecto:
 * Python 3.8+
 * Django 4.0+

## Comando para ejecutar el proyecto

### Activar virtualenv

Para windows:
```
py -m pip install --user virtualenv
py -m venv env
```

### Instalar dependencias

Usando el archivo requirements.txt
```
py -m pip install -r requirements.txt
```

### Para finalizar, ejecute:

```
python manage.py runserver
```