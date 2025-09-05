from fastapi import FastAPI, APIRouter, HTTPException, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import ssl
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import json
import jwt
from passlib.context import CryptContext
from io import BytesIO
import base64
import hashlib


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL')

print(f"🔍 Checking MONGO_URL environment variable...")
print(f"🔍 MONGO_URL exists: {'MONGO_URL' in os.environ}")
print(f"🔍 MONGO_URL value: {mongo_url[:30] if mongo_url else 'None'}...")

if mongo_url:
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'gestion_db')]
    print(f"✅ MongoDB connected: {mongo_url[:30]}...")
else:
    client = None
    db = None
    print("⚠️ MongoDB not connected - running in demo mode")

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key-change-in-production"

# Helper functions for MongoDB serialization
def prepare_for_mongo(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
    return data

def parse_from_mongo(item):
    if isinstance(item, dict):
        for key, value in item.items():
            if isinstance(value, str) and 'T' in value:
                try:
                    item[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                except:
                    pass
    return item

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = await db.users.find_one({"id": payload.get("user_id")})
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    return User(**parse_from_mongo(user))

async def get_admin_user(current_user: "User" = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requieren permisos de administrador")
    return current_user


# Define Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str
    dni: str
    edad: int
    ocupacion: str
    estado_civil: str
    dependientes: int = 0
    password_hash: Optional[str] = None
    is_admin: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str
    dni: str
    edad: int
    ocupacion: str
    estado_civil: str
    dependientes: int = 0
    password: str
    is_admin: bool = False

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str
    dni: str
    edad: int
    ocupacion: str
    estado_civil: str
    dependientes: int
    is_admin: bool
    created_at: datetime

class Ingreso(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    tipo: str  # salario, freelance, inversion, otro
    descripcion: str
    monto: float
    frecuencia: str  # mensual, quincenal, semanal, anual
    activo: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class IngresoCreate(BaseModel):
    tipo: str
    descripcion: str
    monto: float
    frecuencia: str
    activo: bool = True

class Gasto(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    categoria: str  # vivienda, alimentacion, transporte, salud, entretenimiento, otros
    descripcion: str
    monto: float
    frecuencia: str  # mensual, quincenal, semanal, anual
    tipo: str  # fijo, variable
    activo: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class GastoCreate(BaseModel):
    categoria: str
    descripcion: str
    monto: float
    frecuencia: str
    tipo: str
    activo: bool = True

class SimulacionCredito(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    tipo_credito: str  # personal, hipotecario, vehicular
    monto_solicitado: float
    plazo_meses: int
    tasa_interes: float
    cuota_mensual: float
    total_pagar: float
    score_crediticio: float
    aprobado: bool
    observaciones: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SimulacionCreditoCreate(BaseModel):
    tipo_credito: str
    monto_solicitado: float
    plazo_meses: int

class FlujoDinero(BaseModel):
    user_id: str
    ingresos_totales: float
    gastos_totales: float
    flujo_neto: float
    capacidad_ahorro: float
    porcentaje_ahorro: float
    fecha_calculo: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SugerenciaFinanciamiento(BaseModel):
    user_id: str
    tipo: str
    descripcion: str
    monto_sugerido: float
    beneficio: str
    prioridad: int  # 1=alta, 2=media, 3=baja

class CalculoTributario(BaseModel):
    user_id: str
    ingresos_anuales: float
    gastos_deducibles: float
    base_imponible: float
    impuesto_renta: float
    porcentaje_impuesto: float
    tramo_tributario: str
    fecha_calculo: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ReporteSunat(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    tipo_reporte: str
    periodo: str
    datos: Dict[str, Any]
    archivo_base64: Optional[str] = None
    nombre_archivo: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Utility functions
def calcular_cuota_mensual(monto: float, tasa_anual: float, plazo_meses: int) -> float:
    """Calcula la cuota mensual usando la fórmula de amortización francesa"""
    tasa_mensual = tasa_anual / 100 / 12
    if tasa_mensual == 0:
        return monto / plazo_meses
    
    cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** plazo_meses) / ((1 + tasa_mensual) ** plazo_meses - 1)
    return round(cuota, 2)

def calcular_score_crediticio(ingresos: float, gastos: float, edad: int, dependientes: int) -> float:
    """Calcula un score crediticio básico"""
    flujo_neto = ingresos - gastos
    if ingresos == 0:
        return 0
    
    score = 500  # Base score
    
    # Factor de flujo neto
    ratio_flujo = flujo_neto / ingresos
    if ratio_flujo > 0.3:
        score += 200
    elif ratio_flujo > 0.15:
        score += 100
    elif ratio_flujo > 0:
        score += 50
    else:
        score -= 100
    
    # Factor de edad
    if 25 <= edad <= 55:
        score += 50
    elif edad < 25 or edad > 65:
        score -= 30
    
    # Factor de dependientes
    if dependientes <= 2:
        score += 30
    else:
        score -= dependientes * 10
    
    return min(max(score, 300), 850)  # Score entre 300 y 850

def calcular_impuesto_renta(ingresos_anuales: float, gastos_deducibles: float = 0) -> CalculoTributario:
    """Calcula el impuesto a la renta según las tablas tributarias de Perú 2024"""
    # UIT 2024 = S/ 5,150
    UIT = 5150
    
    # Base imponible
    base_imponible = max(0, ingresos_anuales - gastos_deducibles)
    
    # Tabla de impuesto a la renta para personas naturales 2024
    impuesto = 0
    porcentaje = 0
    tramo = ""
    
    if base_imponible <= 5 * UIT:  # Hasta S/ 25,750
        impuesto = 0
        porcentaje = 0
        tramo = "Exonerado (hasta 5 UIT)"
    elif base_imponible <= 20 * UIT:  # Hasta S/ 103,000
        exceso = base_imponible - (5 * UIT)
        impuesto = exceso * 0.08
        porcentaje = 8
        tramo = "Primer tramo (8%)"
    elif base_imponible <= 35 * UIT:  # Hasta S/ 180,250
        base_8 = 15 * UIT * 0.08  # S/ 6,180
        exceso = base_imponible - (20 * UIT)
        impuesto = base_8 + (exceso * 0.14)
        porcentaje = 14
        tramo = "Segundo tramo (14%)"
    elif base_imponible <= 45 * UIT:  # Hasta S/ 231,750
        base_8 = 15 * UIT * 0.08
        base_14 = 15 * UIT * 0.14
        exceso = base_imponible - (35 * UIT)
        impuesto = base_8 + base_14 + (exceso * 0.17)
        porcentaje = 17
        tramo = "Tercer tramo (17%)"
    else:  # Más de S/ 231,750
        base_8 = 15 * UIT * 0.08
        base_14 = 15 * UIT * 0.14
        base_17 = 10 * UIT * 0.17
        exceso = base_imponible - (45 * UIT)
        impuesto = base_8 + base_14 + base_17 + (exceso * 0.30)
        porcentaje = 30
        tramo = "Cuarto tramo (30%)"
    
    return {
        "ingresos_anuales": round(ingresos_anuales, 2),
        "gastos_deducibles": round(gastos_deducibles, 2),
        "base_imponible": round(base_imponible, 2),
        "impuesto_renta": round(impuesto, 2),
        "porcentaje_impuesto": porcentaje,
        "tramo_tributario": tramo
    }

def generar_reporte_csv(datos: dict, tipo_reporte: str) -> str:
    """Genera un reporte en formato CSV y lo convierte a base64"""
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    if tipo_reporte == "ingresos":
        writer.writerow(["Tipo", "Descripción", "Monto", "Frecuencia"])
        for ingreso in datos.get("detalle_ingresos", []):
            writer.writerow([ingreso["tipo"], ingreso["descripcion"], ingreso["monto"], ingreso["frecuencia"]])
    elif tipo_reporte == "gastos":
        writer.writerow(["Categoría", "Descripción", "Monto", "Tipo", "Frecuencia"])
        for gasto in datos.get("detalle_gastos", []):
            writer.writerow([gasto["categoria"], gasto["descripcion"], gasto["monto"], gasto["tipo"], gasto.get("frecuencia", "mensual")])
    else:  # completo
        writer.writerow(["RESUMEN FINANCIERO"])
        writer.writerow(["Ingresos Totales", datos["resumen_financiero"]["ingresos_totales"]])
        writer.writerow(["Gastos Totales", datos["resumen_financiero"]["gastos_totales"]])
        writer.writerow(["Flujo Neto", datos["resumen_financiero"]["flujo_neto"]])
        writer.writerow([])
        writer.writerow(["DETALLE INGRESOS"])
        writer.writerow(["Tipo", "Descripción", "Monto", "Frecuencia"])
        for ingreso in datos.get("detalle_ingresos", []):
            writer.writerow([ingreso["tipo"], ingreso["descripcion"], ingreso["monto"], ingreso["frecuencia"]])
        writer.writerow([])
        writer.writerow(["DETALLE GASTOS"])
        writer.writerow(["Categoría", "Descripción", "Monto", "Tipo", "Frecuencia"])
        for gasto in datos.get("detalle_gastos", []):
            writer.writerow([gasto["categoria"], gasto["descripcion"], gasto["monto"], gasto["tipo"], gasto.get("frecuencia", "mensual")])
    
    csv_content = output.getvalue()
    output.close()
    
    # Convertir a base64
    return base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')


# Authentication Routes
@api_router.post("/register")
async def register_user(user: UserCreate):
    # Verificar si el email ya existe
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Hash password
    password_hash = hash_password(user.password)
    
    user_dict = user.dict()
    user_dict.pop("password")
    user_dict["password_hash"] = password_hash
    
    user_obj = User(**user_dict)
    user_data = prepare_for_mongo(user_obj.dict())
    await db.users.insert_one(user_data)
    
    # Crear token
    token = create_access_token({"user_id": user_obj.id, "email": user_obj.email})
    
    return {
        "user": UserResponse(**user_obj.dict()),
        "access_token": token,
        "token_type": "bearer"
    }

@api_router.post("/login")
async def login(user_login: UserLogin):
    user = await db.users.find_one({"email": user_login.email})
    if not user or not verify_password(user_login.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    
    token = create_access_token({"user_id": user["id"], "email": user["email"]})
    
    return {
        "user": UserResponse(**parse_from_mongo(user)),
        "access_token": token,
        "token_type": "bearer"
    }

@api_router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse(**current_user.dict())


# Admin Routes
@api_router.get("/admin/users", response_model=List[UserResponse])
async def get_all_users_admin(admin_user: User = Depends(get_admin_user)):
    users = await db.users.find().to_list(1000)
    return [UserResponse(**parse_from_mongo(user)) for user in users]

@api_router.get("/admin/stats")
async def get_admin_stats(admin_user: User = Depends(get_admin_user)):
    total_users = await db.users.count_documents({})
    total_ingresos = await db.ingresos.count_documents({})
    total_gastos = await db.gastos.count_documents({})
    total_simulaciones = await db.simulaciones.count_documents({})
    
    return {
        "total_usuarios": total_users,
        "total_ingresos": total_ingresos,
        "total_gastos": total_gastos,
        "total_simulaciones": total_simulaciones
    }


# Routes for Ingresos
@api_router.post("/ingresos", response_model=Ingreso)
async def create_ingreso(ingreso: IngresoCreate, current_user: User = Depends(get_current_user)):
    ingreso_dict = ingreso.dict()
    ingreso_dict["user_id"] = current_user.id
    ingreso_obj = Ingreso(**ingreso_dict)
    ingreso_data = prepare_for_mongo(ingreso_obj.dict())
    await db.ingresos.insert_one(ingreso_data)
    return ingreso_obj

@api_router.get("/ingresos", response_model=List[Ingreso])
async def get_ingresos(current_user: User = Depends(get_current_user)):
    ingresos = await db.ingresos.find({"user_id": current_user.id}).to_list(1000)
    return [Ingreso(**parse_from_mongo(ingreso)) for ingreso in ingresos]

@api_router.delete("/ingresos/{ingreso_id}")
async def delete_ingreso(ingreso_id: str, current_user: User = Depends(get_current_user)):
    result = await db.ingresos.delete_one({"id": ingreso_id, "user_id": current_user.id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")
    return {"message": "Ingreso eliminado"}


# Routes for Gastos
@api_router.post("/gastos", response_model=Gasto)
async def create_gasto(gasto: GastoCreate, current_user: User = Depends(get_current_user)):
    gasto_dict = gasto.dict()
    gasto_dict["user_id"] = current_user.id
    gasto_obj = Gasto(**gasto_dict)
    gasto_data = prepare_for_mongo(gasto_obj.dict())
    await db.gastos.insert_one(gasto_data)
    return gasto_obj

@api_router.get("/gastos", response_model=List[Gasto])
async def get_gastos(current_user: User = Depends(get_current_user)):
    gastos = await db.gastos.find({"user_id": current_user.id}).to_list(1000)
    return [Gasto(**parse_from_mongo(gasto)) for gasto in gastos]

@api_router.delete("/gastos/{gasto_id}")
async def delete_gasto(gasto_id: str, current_user: User = Depends(get_current_user)):
    result = await db.gastos.delete_one({"id": gasto_id, "user_id": current_user.id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return {"message": "Gasto eliminado"}


# Routes for Flujo de Dinero
@api_router.get("/flujo-dinero", response_model=FlujoDinero)
async def calcular_flujo_dinero(current_user: User = Depends(get_current_user)):
    # Obtener ingresos activos
    ingresos = await db.ingresos.find({"user_id": current_user.id, "activo": True}).to_list(1000)
    
    # Obtener gastos activos
    gastos = await db.gastos.find({"user_id": current_user.id, "activo": True}).to_list(1000)
    
    # Convertir todo a mensual
    def convertir_a_mensual(monto: float, frecuencia: str) -> float:
        conversiones = {
            "semanal": monto * 4.33,
            "quincenal": monto * 2,
            "mensual": monto,
            "anual": monto / 12
        }
        return conversiones.get(frecuencia, monto)
    
    ingresos_totales = sum(convertir_a_mensual(i["monto"], i["frecuencia"]) for i in ingresos)
    gastos_totales = sum(convertir_a_mensual(g["monto"], g["frecuencia"]) for g in gastos)
    
    flujo_neto = ingresos_totales - gastos_totales
    capacidad_ahorro = max(0, flujo_neto)
    porcentaje_ahorro = (capacidad_ahorro / ingresos_totales * 100) if ingresos_totales > 0 else 0
    
    return FlujoDinero(
        user_id=current_user.id,
        ingresos_totales=round(ingresos_totales, 2),
        gastos_totales=round(gastos_totales, 2),
        flujo_neto=round(flujo_neto, 2),
        capacidad_ahorro=round(capacidad_ahorro, 2),
        porcentaje_ahorro=round(porcentaje_ahorro, 2)
    )


# Routes for Simulación de Crédito
@api_router.post("/simulacion-credito", response_model=SimulacionCredito)
async def simular_credito(simulacion: SimulacionCreditoCreate, current_user: User = Depends(get_current_user)):
    # Obtener flujo de dinero
    flujo_response = await calcular_flujo_dinero(current_user)
    
    # Tasas de interés por tipo de crédito (anuales)
    tasas = {
        "personal": 25.0,
        "hipotecario": 8.5,
        "vehicular": 15.0
    }
    
    tasa_interes = tasas.get(simulacion.tipo_credito, 20.0)
    cuota_mensual = calcular_cuota_mensual(simulacion.monto_solicitado, tasa_interes, simulacion.plazo_meses)
    total_pagar = cuota_mensual * simulacion.plazo_meses
    
    # Calcular score crediticio
    score = calcular_score_crediticio(
        flujo_response.ingresos_totales,
        flujo_response.gastos_totales,
        current_user.edad,
        current_user.dependientes
    )
    
    # Determinar aprobación
    capacidad_pago = flujo_response.flujo_neto * 0.3  # Máximo 30% del flujo neto
    aprobado = cuota_mensual <= capacidad_pago and score >= 500
    
    observaciones = ""
    if not aprobado:
        if cuota_mensual > capacidad_pago:
            observaciones += "Cuota mensual excede capacidad de pago. "
        if score < 500:
            observaciones += "Score crediticio insuficiente. "
    else:
        observaciones = "Crédito pre-aprobado sujeto a verificación de documentos."
    
    simulacion_obj = SimulacionCredito(
        user_id=current_user.id,
        tipo_credito=simulacion.tipo_credito,
        monto_solicitado=simulacion.monto_solicitado,
        plazo_meses=simulacion.plazo_meses,
        tasa_interes=tasa_interes,
        cuota_mensual=cuota_mensual,
        total_pagar=total_pagar,
        score_crediticio=score,
        aprobado=aprobado,
        observaciones=observaciones
    )
    
    simulacion_data = prepare_for_mongo(simulacion_obj.dict())
    await db.simulaciones.insert_one(simulacion_data)
    return simulacion_obj

@api_router.get("/simulaciones", response_model=List[SimulacionCredito])
async def get_simulaciones(current_user: User = Depends(get_current_user)):
    simulaciones = await db.simulaciones.find({"user_id": current_user.id}).to_list(1000)
    return [SimulacionCredito(**parse_from_mongo(sim)) for sim in simulaciones]


# Routes for Cálculo Tributario
@api_router.get("/calculo-tributario")
async def calcular_tributario(current_user: User = Depends(get_current_user)):
    # Obtener flujo de dinero
    flujo_response = await calcular_flujo_dinero(current_user)
    
    # Calcular ingresos anuales
    ingresos_anuales = flujo_response.ingresos_totales * 12
    
    # Gastos deducibles (asumimos 20% de los gastos totales como deducibles)
    gastos_deducibles = (flujo_response.gastos_totales * 12) * 0.2
    
    # Calcular impuesto
    calculo = calcular_impuesto_renta(ingresos_anuales, gastos_deducibles)
    
    # Agregar datos del usuario
    calculo["user_id"] = current_user.id
    calculo["fecha_calculo"] = datetime.now(timezone.utc)
    
    return CalculoTributario(**calculo)


# Routes for Sugerencias
@api_router.get("/sugerencias", response_model=List[SugerenciaFinanciamiento])
async def get_sugerencias(current_user: User = Depends(get_current_user)):
    flujo = await calcular_flujo_dinero(current_user)
    sugerencias = []
    
    if flujo.porcentaje_ahorro < 10:
        sugerencias.append(SugerenciaFinanciamiento(
            user_id=current_user.id,
            tipo="Ahorro de Emergencia",
            descripcion="Se recomienda ahorrar al menos el 10% de tus ingresos para emergencias",
            monto_sugerido=flujo.ingresos_totales * 0.1,
            beneficio="Protección financiera ante imprevistos",
            prioridad=1
        ))
    
    if flujo.capacidad_ahorro > 500:
        sugerencias.append(SugerenciaFinanciamiento(
            user_id=current_user.id,
            tipo="Inversión",
            descripcion="Considera invertir tu excedente en instrumentos financieros",
            monto_sugerido=flujo.capacidad_ahorro * 0.5,
            beneficio="Crecimiento de patrimonio a largo plazo",
            prioridad=2
        ))
    
    if flujo.flujo_neto < 0:
        sugerencias.append(SugerenciaFinanciamiento(
            user_id=current_user.id,
            tipo="Reducción de Gastos",
            descripcion="Tus gastos superan tus ingresos. Revisa y reduce gastos no esenciales",
            monto_sugerido=abs(flujo.flujo_neto),
            beneficio="Equilibrio financiero y evitar deudas",
            prioridad=1
        ))
    
    return sugerencias


# Routes for Reportes SUNAT
@api_router.post("/reporte-sunat")
async def generar_reporte_sunat(tipo_reporte: str, periodo: str, current_user: User = Depends(get_current_user)):
    flujo = await calcular_flujo_dinero(current_user)
    ingresos = await db.ingresos.find({"user_id": current_user.id, "activo": True}).to_list(1000)
    gastos = await db.gastos.find({"user_id": current_user.id, "activo": True}).to_list(1000)
    
    # Generar datos del reporte
    datos_reporte = {
        "dni": current_user.dni,
        "nombre_completo": f"{current_user.nombre} {current_user.apellido}",
        "periodo": periodo,
        "tipo_reporte": tipo_reporte,
        "resumen_financiero": {
            "ingresos_totales": flujo.ingresos_totales,
            "gastos_totales": flujo.gastos_totales,
            "flujo_neto": flujo.flujo_neto
        },
        "detalle_ingresos": [
            {
                "tipo": ing["tipo"],
                "descripcion": ing["descripcion"],
                "monto": ing["monto"],
                "frecuencia": ing["frecuencia"]
            } for ing in ingresos
        ],
        "detalle_gastos": [
            {
                "categoria": gasto["categoria"],
                "descripcion": gasto["descripcion"],
                "monto": gasto["monto"],
                "tipo": gasto["tipo"]
            } for gasto in gastos
        ]
    }
    
    # Generar archivo CSV
    archivo_base64 = generar_reporte_csv(datos_reporte, tipo_reporte)
    nombre_archivo = f"reporte_{tipo_reporte}_{periodo}_{current_user.dni}.csv"
    
    reporte_obj = ReporteSunat(
        user_id=current_user.id,
        tipo_reporte=tipo_reporte,
        periodo=periodo,
        datos=datos_reporte,
        archivo_base64=archivo_base64,
        nombre_archivo=nombre_archivo
    )
    
    reporte_data = prepare_for_mongo(reporte_obj.dict())
    await db.reportes_sunat.insert_one(reporte_data)
    return reporte_obj

@api_router.get("/reportes-sunat", response_model=List[ReporteSunat])
async def get_reportes_sunat(current_user: User = Depends(get_current_user)):
    reportes = await db.reportes_sunat.find({"user_id": current_user.id}).to_list(1000)
    return [ReporteSunat(**parse_from_mongo(reporte)) for reporte in reportes]

@api_router.get("/reportes-sunat/{reporte_id}/download")
async def download_reporte(reporte_id: str, current_user: User = Depends(get_current_user)):
    reporte = await db.reportes_sunat.find_one({"id": reporte_id, "user_id": current_user.id})
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    
    # Decodificar el archivo base64
    archivo_content = base64.b64decode(reporte["archivo_base64"])
    
    return Response(
        content=archivo_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={reporte['nombre_archivo']}"}
    )


# Include the router in the main app
app.include_router(api_router)

# Health check route for Railway (outside of /api prefix)
@app.get("/")
async def health_check():
    mongo_status = "connected" if db is not None else "not connected"
    return {
        "status": "OK", 
        "message": "API de Finanzas Personales funcionando correctamente",
        "mongodb": mongo_status,
        "environment": {
            "SECRET_KEY": "configured" if os.environ.get('SECRET_KEY') else "missing",
            "DB_NAME": os.environ.get('DB_NAME', 'not set'),
            "MONGO_URL": "configured" if os.environ.get('MONGO_URL') else "missing"
        }
    }

# Debug endpoint to see database collections and counts
@app.get("/debug/db")
async def debug_database():
    if db is None:
        return {"error": "Database not connected", "mongo_url_configured": "MONGO_URL" in os.environ}
    
    try:
        # Simple ping test first
        await db.admin.command('ping')
        
        # Get database stats
        stats = await db.command("dbStats")
        
        # Try to get collections with error handling
        try:
            collections = await db.list_collection_names()
        except Exception as e:
            return {
                "error": f"Could not list collections: {str(e)}",
                "db_ping": "success",
                "db_stats": {
                    "db_name": stats.get("db", "unknown"),
                    "collections": stats.get("collections", 0),
                    "objects": stats.get("objects", 0)
                }
            }
        
        result = {
            "database_name": db.name,
            "db_ping": "success",
            "total_collections": len(collections),
            "collections": collections,
            "db_stats": {
                "objects_count": stats.get("objects", 0),
                "storage_size": stats.get("storageSize", 0),
                "indexes": stats.get("indexes", 0)
            }
        }
        
        # Try to count users specifically
        try:
            if "users" in collections:
                users_count = await db.users.count_documents({})
                result["users_count"] = users_count
            else:
                result["users_count"] = 0
        except Exception as e:
            result["users_count_error"] = str(e)
        
        return result
        
    except Exception as e:
        return {
            "error": f"Database connection failed: {str(e)}",
            "mongo_url_present": "MONGO_URL" in os.environ,
            "db_object": db is not None
        }

# Health check route (with /api prefix)
@api_router.get("/")
async def root():
    return {"message": "API de Finanzas Personales funcionando correctamente"}

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()