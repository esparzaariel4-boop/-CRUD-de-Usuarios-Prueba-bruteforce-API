# CRUD de Usuarios + Prueba controlada de fuerza bruta contra tu propia API

## Descripción
Este proyecto implementa una **API REST básica** usando FastAPI para gestionar usuarios y realizar login. La base de datos está simulada en memoria (lista de usuarios dentro del código), lo que permite entender la lógica sin usar una base de datos real.

También incluye un archivo `ataque.py` que demuestra de forma académica cómo funciona un ataque de fuerza bruta sobre contraseñas simples, para comprender la importancia de la seguridad.

---

## Archivos del proyecto

```
main.py
ataque.py
requirements.txt
README.md
```

### main.py
Contiene la lógica principal de la API. En este archivo se crea la aplicación con FastAPI, se definen los modelos de datos y se programan las rutas para crear, consultar, actualizar, eliminar usuarios y realizar el login.

### ataque.py
Contiene una demostración del **ataque de fuerza bruta con `itertools`**. Este archivo prueba combinaciones de caracteres hasta encontrar una contraseña corta de ejemplo. Su propósito es académico, para mostrar por qué una contraseña débil puede ser vulnerable.

### requirements.txt
Dependencias necesarias:
```
fastapi[standard]
sqlmodel
```

---

## Instalación

Crear entorno virtual:
```
python -m venv venv
source .venv/bin/activate
```

Instalar dependencias:
```
pip install -r requirements.txt
```

Ejecutar API:
```
uvicorn main:app --reload
```

Abrir documentación:
```
http://127.0.0.1:8000/docs
```

---

## Explicación del código `main.py`

El archivo `main.py` es el núcleo del proyecto.

### Importaciones
- `FastAPI`: crea la API.
- `HTTPException`: permite enviar errores, por ejemplo cuando un usuario no existe.
- `SQLModel`: sirve para definir los modelos de datos.
- `Optional`: indica que algunos campos pueden estar vacíos.
- `time`: se usa para controlar el bloqueo temporal en el login.

### Modelos
En el código se definen cuatro modelos:
- `User`: representa un usuario completo.
- `UserCreate`: se usa al crear un nuevo usuario.
- `UserUpdate`: se usa al actualizar datos, por eso sus campos son opcionales.
- `LoginData`: contiene username y password para el inicio de sesión.

### Base de datos en memoria
Los usuarios están guardados en una lista llamada `db_users`. Esto significa que no hay una base de datos real, sino datos temporales cargados directamente en el programa.

### Funciones principales
- `GET /`: comprueba que la API está funcionando.
- `POST /users`: crea un usuario nuevo.
- `GET /users`: devuelve todos los usuarios.
- `GET /users/{id}`: busca un usuario por ID.
- `PUT /users/{id}`: actualiza datos del usuario.
- `DELETE /users/{id}`: elimina un usuario.
- `POST /login`: valida credenciales.

### Lógica del login
El login compara el nombre de usuario y la contraseña con los datos guardados en memoria. Si el usuario falla muchas veces, se registra el número de intentos en `failed_attempts` y se bloquea temporalmente usando `blocked_users`. En este caso, el límite es de 5 intentos y el tiempo de bloqueo es de 30 segundos.

---

## Explicación del código `ataque.py`

Este archivo muestra un **ataque de fuerza bruta con `itertools`**.

### ¿Qué hace?
Intenta descubrir una contraseña probando muchas combinaciones posibles de letras mayúsculas, minúsculas y números, hasta encontrar la correcta.

### Importaciones
- `itertools`: se usa para generar combinaciones automáticamente.
- `time`: mide cuánto tarda el proceso.

### ¿Qué es `itertools`?
`itertools` es un módulo de Python que ofrece herramientas para trabajar con iteradores y combinaciones de datos de forma eficiente. En este proyecto se usa porque permite generar todas las posibles combinaciones de caracteres sin tener que escribir muchos ciclos manualmente.

La función más importante aquí es:
- `itertools.product(...)`: genera el producto cartesiano entre los elementos. En este caso, produce todas las combinaciones posibles de caracteres para una longitud determinada.

Por ejemplo, si el alfabeto fuera `ab` y la longitud fuera 2, `product` generaría:
- `aa`
- `ab`
- `ba`
- `bb`

### Cómo funciona el ataque
1. Se define un alfabeto con letras y números.
2. Se recorre desde longitud 1 hasta la longitud de la contraseña real.
3. Con `itertools.product`, se generan todas las combinaciones posibles.
4. Cada combinación se une con `"".join(...)` para formar un intento.
5. Si el intento coincide con la contraseña, el programa se detiene y muestra el resultado.

### Qué enseña este código
Este archivo ayuda a entender que:
- una contraseña corta es más fácil de descubrir,
- mientras más combinaciones existan, más tiempo puede tardar,
- y por eso en sistemas reales se necesitan contraseñas fuertes y límites de intentos.

---

## Endpoints principales

| Método | Ruta | Función |
|-------|------|--------|
| GET | / | Verifica API |
| POST | /users | Crear usuario |
| GET | /users | Listar usuarios |
| GET | /users/{id} | Obtener usuario |
| PUT | /users/{id} | Actualizar usuario |
| DELETE | /users/{id} | Eliminar usuario |
| POST | /login | Iniciar sesión |

---

## Ejemplo login

Solicitud:
```
POST /login
{
 "username": "admin",
 "password": "abc"
}
```

Respuesta:
```
Login successful
```

Si se superan 5 intentos fallidos, el usuario se bloquea por 30 segundos.

---

## Conceptos aprendidos
- creación de API con FastAPI
- modelos con SQLModel
- operaciones CRUD
- validación de datos
- manejo de errores HTTP
- lógica básica de autenticación
- importancia de contraseñas seguras

---

## Conclusión
Este proyecto permite entender la estructura básica de un sistema de autenticación. Aunque es una versión sencilla, muestra cómo funcionan las rutas, validaciones y controles de seguridad iniciales en una API backend.

