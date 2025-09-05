import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def check_database():
    # URL de la base de datos de Railway
    mongo_url = "https://gestion-presupuesto-production.up.railway.app"
    
    print("🔍 Conectando a la base de datos...")
    print(f"📍 URL: {mongo_url}")
    
    try:
        # Hacer una petición GET a la API para verificar el estado
        import requests
        
        response = requests.get(mongo_url)
        data = response.json()
        
        print("\n✅ Estado de la API:")
        print(f"🔗 Status: {data.get('status')}")
        print(f"🗄️ MongoDB: {data.get('mongodb')}")
        
        # Si MongoDB está conectado, podemos hacer consultas a través de la API
        if data.get('mongodb') == 'connected':
            print("\n🎉 ¡MongoDB está conectado!")
            
            # Intentar obtener usuarios a través de la API
            try:
                # Esta sería la URL de la API para obtener usuarios
                users_url = f"{mongo_url}/api/users"
                print(f"📊 Consultando usuarios en: {users_url}")
                
                # Nota: Esto requerirá autenticación, pero podemos ver la respuesta
                users_response = requests.get(users_url)
                print(f"📈 Respuesta usuarios: {users_response.status_code}")
                
                if users_response.status_code == 401:
                    print("🔐 Se requiere autenticación para ver usuarios (¡esto es bueno!)")
                elif users_response.status_code == 200:
                    users_data = users_response.json()
                    print(f"👥 Usuarios encontrados: {len(users_data)}")
                else:
                    print(f"🤔 Respuesta: {users_response.text[:200]}")
                    
            except Exception as e:
                print(f"⚠️ No se pudo consultar usuarios: {e}")
        else:
            print("❌ MongoDB no está conectado")
            
    except Exception as e:
        print(f"❌ Error al conectar: {e}")

if __name__ == "__main__":
    asyncio.run(check_database())
