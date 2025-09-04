# Sistema de Gestión de Presupuesto Personal

Una aplicación completa de gestión financiera personal construida con FastAPI (backend) y React (frontend).

## 🚀 Deploy en Railway

### Paso 1: Preparación
1. Sube este proyecto a GitHub
2. Crea una cuenta en [railway.app](https://railway.app)

### Paso 2: Deploy del Backend
1. En Railway, crea un nuevo proyecto
2. Conecta tu repositorio de GitHub  
3. Railway detectará automáticamente Python y usará `railway.json`
4. Añade las variables de entorno:
   - `SECRET_KEY`: una clave secreta fuerte
   - `DB_NAME`: gestion_db

### Paso 3: Añadir MongoDB
1. En tu proyecto Railway, añade MongoDB desde la pestaña "Add Service" 
2. Railway automáticamente creará la variable `MONGO_URL`

### Paso 4: Deploy del Frontend  
1. Crea otro servicio en Railway para el frontend
2. Configura la ruta: `frontend/`
3. Añade la variable de entorno:
   - `REACT_APP_BACKEND_URL`: La URL de tu backend Railway

## 🛠️ Desarrollo Local

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --reload --port 8000
```

### Frontend  
```bash
cd frontend
npm install
npm start
```

## 📋 Características

- ✅ Autenticación JWT
- ✅ Gestión de ingresos y gastos  
- ✅ Simulador de créditos
- ✅ Cálculo de impuestos
- ✅ Dashboard interactivo
- ✅ Exportación a CSV
- ✅ Interfaz moderna con Tailwind CSS

## 🔧 Stack Tecnológico

**Backend:**
- FastAPI
- MongoDB (Motor - async driver)
- JWT Authentication  
- Bcrypt password hashing

**Frontend:**
- React 19
- Tailwind CSS
- shadcn/ui components
- Axios

**Deployment:**
- Railway.app (Backend + MongoDB)
- Vercel (Frontend) - opcional
