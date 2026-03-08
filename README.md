# FitLife Backend

API REST para gestión de usuarios, autenticación JWT y evaluaciones físicas. Construida con **FastAPI**, **SQLAlchemy async** y arquitectura hexagonal.

---

## 🚀 Levantar el servidor

```bash
# Activar entorno virtual (Windows)
.venv\Scripts\activate

# Correr servidor en modo desarrollo
uvicorn src.main:app --reload
```

El servidor queda disponible en: `http://127.0.0.1:8000`

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Health check**: http://127.0.0.1:8000/healthz

---

## 🧪 Ejecutar tests

### Todos los tests
```bash
pytest -v
```

### Solo integración
```bash
pytest tests/integration/ -v
```

### Solo unitarios
```bash
pytest tests/unit/ -v
```

### Con reporte de cobertura
```bash
pytest --cov=src --cov-report=term-missing
```

### Un test específico
```bash
pytest tests/integration/test_assessment_flow.py -v
pytest tests/integration/test_auth_flow.py -v
```

---

## 🎨 Formateo y linting

### Black (formatear código)
```bash
# Ver qué cambiaría sin modificar nada
black src tests --check

# Aplicar formateo
black src tests

flake8 src tests
```

### Isort (ordenar imports)
```bash
isort src tests --check
isort src tests
```

### Flake8 (linting)
```bash
flake8 src tests
```

---

## 🗃️ Base de datos

### Inicializar / recrear tablas
```bash
python -m src.scripts.init_db
```

---

## 📡 Endpoints principales

### Auth
| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/auth/register` | Registrar usuario |
| `POST` | `/api/auth/login` | Iniciar sesión |
| `POST` | `/api/auth/refresh` | Refrescar access token |

### Assessments
| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/assessments/submit` | Enviar evaluación física *(requiere auth)* |

---

## 🔐 Ejemplo de flujo completo (curl)

```bash
# 1. Registrar usuario
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "Password123"}'

# 2. Login
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "Password123"}'

# 3. Enviar assessment (usa el access_token del paso 2)
curl -X POST http://127.0.0.1:8000/api/assessments/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "goal": "muscle_gain",
    "activity_level": "moderately_active",
    "experience_level": "intermediate",
    "height_cm": 175,
    "weight_kg": 70,
    "age": 25
  }'
```

---

## 📁 Estructura del proyecto

```
src/
├── adapters/api/          # Rutas, schemas, dependencias FastAPI
├── application/           # Casos de uso y DTOs
│   └── use_cases/
│       ├── auth/          # RegisterUser, LoginUser, RefreshToken
│       └── assessments/   # SubmitAssessment
├── domain/                # Entidades, repositorios, servicios, excepciones
├── infrastructure/        # SQLAlchemy models, repositorios, seguridad
│   ├── database/
│   ├── repositories/
│   └── security/
└── config/                # Settings (pydantic-settings)
tests/
├── integration/           # Tests end-to-end con base de datos en memoria
└── unit/                  # Tests unitarios con mocks
```

---

## ⚙️ Variables de entorno

Crea un archivo `.env` en la raíz (opcional, hay valores por defecto):

```env
SECRET_KEY=tu-clave-secreta-de-al-menos-32-caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
