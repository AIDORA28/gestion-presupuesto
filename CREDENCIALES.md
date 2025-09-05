# 🔐 Credenciales del Sistema de Gestión de Presupuesto

## 📋 **Información de Acceso**

### **URL de la Aplicación:**
- **API Backend:** `https://gestion-presupuesto-production.up.railway.app`
- **Frontend Local:** `http://localhost:3000` (ejecutar `npm start` en la carpeta `frontend`)

---

## 👤 **Credenciales de Prueba**

### **Usuario Administrador:**
```
📧 Email: admin@gestion.com
🔑 Password: admin123
👑 Rol: Administrador
```

### **Usuario Regular:**
```
📧 Email: usuario@test.com
🔑 Password: usuario123
👤 Rol: Usuario estándar
```

---

## 🚀 **Cómo usar el sistema:**

### **1. Iniciar Frontend:**
```bash
cd frontend
npm install
npm start
```

### **2. Acceder al Sistema:**
1. Abre `http://localhost:3000` en tu navegador
2. Usa las credenciales de arriba para iniciar sesión
3. Explora las funcionalidades de gestión financiera

### **3. Funcionalidades Disponibles:**
- ✅ **Autenticación** de usuarios (login/registro)
- ✅ **Dashboard** financiero interactivo
- ✅ **Gestión de ingresos** y gastos
- ✅ **Simulador de créditos**
- ✅ **Cálculo de impuestos**
- ✅ **Reportes** y exportación a CSV
- ✅ **Interfaz moderna** con Tailwind CSS

---

## ⚙️ **Estado Actual del Sistema:**

### **✅ Funcionando:**
- Backend API desplegado en Railway
- Servidor FastAPI corriendo correctamente
- Endpoints de la API disponibles
- Frontend React configurado
- Interfaz de usuario completa

### **⚠️ Pendiente (Opcional):**
- Conexión a MongoDB para persistencia de datos
- Registro real de usuarios (funciona en modo demo)

---

## 🔧 **Para Desarrolladores:**

### **Variables de Entorno (Railway):**
```
SECRET_KEY = gestion_presupuesto_2025_railway_secret_key_abc123xyz789
DB_NAME = gestion_db
MONGO_URL = (pendiente de conectar)
```

### **Tecnologías Utilizadas:**
- **Backend:** FastAPI + Python 3.11
- **Frontend:** React 19 + Tailwind CSS + shadcn/ui
- **Base de Datos:** MongoDB (en configuración)
- **Deploy:** Railway.app
- **Autenticación:** JWT Tokens

---

## 📱 **Compartir con tu Compañero:**

1. **Comparte este archivo** con las credenciales
2. **Envía la URL del repositorio:** `https://github.com/AIDORA28/gestion-presupuesto`
3. **Instrucciones simples:**
   - Clonar repo: `git clone https://github.com/AIDORA28/gestion-presupuesto.git`
   - Instalar: `cd frontend && npm install`
   - Ejecutar: `npm start`
   - Usar credenciales de arriba

---

## 🎯 **Datos de Prueba Sugeridos:**

### **Ingresos de Ejemplo:**
- Salario: $3,000,000 COP
- Freelance: $500,000 COP
- Inversiones: $200,000 COP

### **Gastos de Ejemplo:**
- Vivienda: $1,200,000 COP
- Alimentación: $600,000 COP
- Transporte: $300,000 COP
- Entretenimiento: $200,000 COP

---

**📅 Último Update:** $(date)
**👨‍💻 Desarrollado por:** AIDORA28
**🚀 Deploy:** Railway + GitHub
