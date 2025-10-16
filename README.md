# ⚙️ Backend API – Django REST Framework

API REST desarrollada con **Django + Django REST Framework (DRF)**.  
Incluye autenticación **JWT**, manejo de **roles y permisos**, y endpoints bien estructurados con documentación interactiva (**Swagger**, **ReDoc** y **Scalar Docs**).

---

## 🚀 Características principales

✅ **Autenticación JWT** (login / refresh / perfil autenticado)  
✅ **CustomUser Model** (usuario personalizado por correo electrónico)  
✅ **Roles y permisos** administrables vía API  
✅ **Respuestas normalizadas** con estructura estándar  
✅ **Documentación interactiva** con Swagger, Redoc y Scalar  
✅ **Soporte para PostgreSQL**  
✅ **Versionado**: `/api/v1/`  
✅ **Filtros, búsqueda y ordenación** integrados (django-filter)  
✅ **Admin panel personalizado** con CustomUser  

---





## 🔐 Autenticación

El sistema usa **JSON Web Tokens (JWT)** para manejar sesiones seguras.

### 🔸 Login
`POST /api/v1/token/`

**Body:**
```json
{
  "email": "usuario@correo.com",
  "password": "123456"
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "refresh": "<token_refresh>",
    "access": "<token_access>",
    "user": {
      "id": 1,
      "email": "usuario@correo.com",
      "role": "admin",
      "permissions": [
        { "id": 1, "name": "usuarios.crear" }
      ]
    }
  },
  "errors": null
}
```

### 🔸 Refrescar token
`POST /api/v1/token/refresh/`

### 🔸 Obtener datos del usuario autenticado
`GET /api/v1/auth/me/`

---

## 🧱 Recursos principales

| Recurso | Descripción | Endpoints |
|----------|--------------|------------|
| 🧑‍💻 **Usuarios** | CRUD de usuarios con rol asignado | `/api/v1/users/` |
| 🛡️ **Roles** | Asignación de permisos de negocio | `/api/v1/roles/` |
| 🔐 **Permisos** | Permisos reutilizables por rol | `/api/v1/permissions/` |
| 👤 **Perfil** | Datos del usuario autenticado | `/api/v1/auth/me/` |

---

## 📦 Instalación y configuración

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/Juanfelipe-pro/backend-api.git
cd backend-api
```

### 2️⃣ Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno
Crea un archivo `.env` en la raíz:
```bash
SECRET_KEY=tu_clave_secreta
DEBUG=True
DB_NAME=portfolio_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 5️⃣ Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Crear superusuario
```bash
python manage.py createsuperuser
```

### 7️⃣ Ejecutar servidor
```bash
python manage.py runserver
```

---

## 📖 Documentación interactiva

| Herramienta | URL |
|--------------|-----|
| ⚡ **Swagger UI** | [http://localhost:8000/](http://localhost:8000/) |
| 📘 **ReDoc** | [http://localhost:8000/redoc/](http://localhost:8000/redoc/) |


---

## 🧠 Estructura estándar de respuesta

Todas las respuestas siguen el siguiente formato:

```json
{
  "success": true|false,
  "message": "Descripción de la operación",
  "data": {...} | null,
  "errors": {...} | null
}
```

---

## 🧰 Tecnologías utilizadas

| Tecnología | Propósito |
|-------------|------------|
| 🐍 **Python 3.12+** | Lenguaje base |
| 🧱 **Django 5+** | Framework web principal |
| 🔗 **Django REST Framework** | API REST |
| 🔐 **SimpleJWT** | Autenticación con tokens |
| 🗃️ **PostgreSQL** | Base de datos |
| 🔍 **django-filter** | Filtros y búsqueda |
| 🧾 **drf-yasg / drf-spectacular** | Generación de documentación OpenAPI |


---

## 📚 Versionado

Actualmente la API se encuentra en:
```
/api/v1/
```
Preparada para futuras versiones (`/api/v2/`, `/api/v3/`, etc.) sin afectar clientes existentes.

---

## 💡 Autor

👨‍💻 **Juan Felipe Alvear**  
📫 [juanfelipealvearestrada@gmail.com](mailto:tuemail@ejemplo.com)  
🌐 [https://github.com/Juanfelipe-pro](https://github.com/Juanfelipe-pro)  

---

## 🪪 Licencia

```
© 2025 Todos los derechos reservados.
Este proyecto puede ser usado libremente con fines educativos o de portafolio.
```
