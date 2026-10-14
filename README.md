# PFO 2: Sistema de Gestión de Tareas con API y Base de Datos

Servidor hecho con Flask que permite registrar usuarios, iniciar sesión y acceder a una página de bienvenida. Los datos se guardan en SQLite y las contraseñas se almacenan hasheadas, nunca en texto plano.

## Objetivos

Al finalizar este trabajo práctico se logra:

1. Implementar una API REST con endpoints funcionales.
2. Utilizar autenticación básica con protección de contraseñas.
3. Gestionar datos persistentes con SQLite.
4. Construir un cliente en consola que interactúe con la API.

### Cómo se cumplen en este proyecto

| Objetivo | Dónde se cumple |
|---|---|
| 1. API REST con endpoints funcionales | `servidor.py` define los endpoints `POST /registro`, `POST /login` y `GET /tareas` con Flask |
| 2. Autenticación básica con protección de contraseñas | El login verifica las credenciales, las contraseñas se guardan hasheadas (`werkzeug.security`) y `/tareas` solo se muestra si el usuario inició sesión |
| 3. Datos persistentes con SQLite | La tabla `usuarios` vive en el archivo `usuarios.db` (módulo `sqlite3`), por lo que los datos siguen ahí aunque se apague el servidor |
| 4. Cliente en consola que interactúa con la API | `cliente.py` ofrece un menú para registrarse, iniciar sesión y ver las tareas |

## Contenido

1. [Instalación](#1-instalación)
2. [Configuración](#2-configuración)
3. [Uso](#3-uso)
4. [Capturas de pantalla](#4-capturas-de-pantalla)
5. [Arquitectura](#5-arquitectura)
6. [Respuestas conceptuales](#6-respuestas-conceptuales)
7. [Publicación en GitHub](#7-publicación-en-github)

## 1. Instalación

### Requisitos previos

- Python 3.9 o superior (`python --version` para comprobarlo).
- `pip`, el gestor de paquetes de Python (viene con Python).
- Git, solo si se va a clonar el repositorio.

### Pasos

1. **Obtener el proyecto.** Clonar el repositorio (o descargarlo como ZIP) y entrar a la carpeta:
   ```
   git clone https://github.com/GimEscalante/pfo2
   cd pfo2
   ```

2. **Crear un entorno virtual**, para no mezclar las librerías con las de otros proyectos:
   ```
   py -m venv venv
   ```
   Activarlo:
   - Windows: `venv\Scripts\activate`
   - Linux / macOS: `source venv/bin/activate`

3. **Instalar las dependencias:**
   ```
   pip install -r requirements.txt
   ```
   Esto instala:
   - `flask`: el framework web del servidor (incluye `werkzeug`, que se usa para hashear contraseñas).
   - `requests`: solo se usa en `cliente.py`.

   SQLite no hay que instalarlo: viene incluido en Python (módulo `sqlite3`).

### Estructura del proyecto

```
servidor.py        # API Flask + SQLite
cliente.py         # cliente en consola (opcional, para probar)
requirements.txt   # dependencias
README.md
capturas/          # capturas de pantalla de las pruebas
```

## 2. Configuración

No hace falta configurar nada para que funcione: el proyecto trae valores por defecto. Si se quiere cambiar algo, estos son los ajustes y dónde están:

| Ajuste | Dónde | Valor por defecto | Para qué sirve |
|---|---|---|---|
| `DB_NAME` | `servidor.py`, arriba del archivo | `usuarios.db` | Nombre del archivo de la base SQLite |
| `app.secret_key` | `servidor.py`, arriba del archivo | `clave-secreta-pfo2` | Clave con la que Flask protege la sesión del usuario. Si el proyecto se usara de verdad, hay que cambiarla por un valor largo y secreto |
| `host` y `port` | `servidor.py`, última línea (`app.run`) | `localhost` y `5000` | Dirección y puerto donde escucha el servidor |
| `debug` | `servidor.py`, última línea (`app.run`) | `True` | Reinicia el servidor al cambiar el código y muestra errores detallados. Para uso real conviene ponerlo en `False` |
| `URL` | `cliente.py`, arriba del archivo | `http://localhost:5000` | Dirección del servidor a la que se conecta el cliente. Si se cambia el puerto del servidor, hay que cambiarlo también acá |

**Base de datos:** no hay que crearla a mano. La primera vez que se inicia el servidor se crea el archivo `usuarios.db` con la tabla `usuarios`. Para empezar de cero, se apaga el servidor y se borra ese archivo.

## 3. Uso

### Iniciar el servidor

```
py servidor.py
```

Queda escuchando en `http://localhost:5000`. Hay que dejar esa terminal abierta mientras se usa el sistema. Para detenerlo se presiona `Ctrl + C`.

### Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| POST | `/registro` | Recibe `{"usuario": "...", "contraseña": "..."}` y guarda el usuario con la contraseña hasheada |
| POST | `/login` | Verifica las credenciales y habilita el acceso a `/tareas` |
| GET | `/tareas` | Muestra un HTML de bienvenida (solo si se inició sesión) |

### Usar el cliente en consola

Con el servidor corriendo, abrir **otra terminal** (con el entorno virtual activado, si se usa) y ejecutar:

```
py cliente.py
```

Aparece un menú:

```
=============================================
        SISTEMA DE GESTIÓN DE TAREAS
=============================================
1. Registrarse
2. Iniciar sesión
3. Ver tareas
4. Salir
=============================================
Seleccione una opción:
```

Pasos típicos: elegir 1 para crear un usuario, luego 2 para iniciar sesión con ese usuario, y 3 para ver la página de bienvenida.

Cada respuesta del servidor se muestra separada del menú, entre líneas y con una etiqueta que indica si salió bien o mal:

```
---------------------------------------------
[OK] Usuario registrado.
---------------------------------------------
```

```
---------------------------------------------
[ERROR] Usuario o contraseña incorrectos.
---------------------------------------------
```

### 4. Resultados esperados

| Prueba | Respuesta |
|---|---|
| Registro correcto | `Usuario registrado.` (201) |
| Registrar un usuario que ya existe | `El usuario ya existe.` (409) |
| Registro con datos faltantes | `Faltan datos: usuario y contraseña.` (400) |
| Login con contraseña incorrecta | `Usuario o contraseña incorrectos.` (401) |
| Login correcto | `Bienvenido, ana.` |
| `/tareas` sin iniciar sesión | `Primero hay que iniciar sesión.` (401) |
| `/tareas` con sesión iniciada | Página HTML de bienvenida |


## 5. Arquitectura

| Componente | En este proyecto |
|---|---|
| Cliente | `cliente.py` (consola), `curl` o el navegador |
| Servidor | `servidor.py` (Flask) |
| Protocolo de comunicación | HTTP, con datos en formato JSON |
| API | Endpoints `/registro`, `/login` y `/tareas` |
| Base de datos | SQLite (`usuarios.db`) |
| Middleware | Autenticación: se verifica la sesión antes de dar acceso a `/tareas` |

## 6. Respuestas conceptuales

### ¿Por qué hashear contraseñas?

Porque así la contraseña real nunca se guarda en la base de datos. Un hash es el resultado de una función matemática de un solo sentido: se puede calcular a partir de la contraseña, pero no se puede revertir para recuperarla. Si alguien roba o accede a la base de datos, solo ve los hashes y no las contraseñas de los usuarios. Esto importa porque muchas personas reutilizan la misma contraseña en varios sitios. Tampoco deja que los propios administradores la vean.

Para comprobar el login, el servidor no desencripta nada: calcula el hash de la contraseña ingresada y lo compara con el hash guardado. La librería usada (`werkzeug.security`) además agrega una *sal* aleatoria a cada hash, de modo que dos usuarios con la misma contraseña terminan con hashes distintos.

### Ventajas de usar SQLite en este proyecto

- **No necesita instalar ni configurar un servidor de base de datos**: toda la base es un solo archivo (`usuarios.db`).
- **Ya viene incluido en Python** (módulo `sqlite3`), sin dependencias extra.
- **Los datos persisten**: si se apaga el servidor, los usuarios siguen ahí, a diferencia de guardar los datos en una lista en memoria.
- **Es simple y liviano**, ideal para un proyecto pequeño o de práctica, y fácil de copiar o entregar junto con el código.

Como limitación, no está pensado para muchos usuarios escribiendo a la vez; para una aplicación grande conviene un motor como MySQL o PostgreSQL.
