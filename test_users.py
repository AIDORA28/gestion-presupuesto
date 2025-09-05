import requests
import json

def check_users():
    base_url = "https://gestion-presupuesto-production.up.railway.app"
    
    print("🔍 Verificando usuarios en la base de datos...")
    print(f"📍 API: {base_url}")
    
    # Primero registremos un usuario de prueba para verificar que funciona
    print("\n1️⃣ Intentando registrar un usuario de prueba...")
    
    register_data = {
        "username": "test_user",
        "email": "test@example.com", 
        "password": "test123",
        "is_admin": False
    }
    
    try:
        response = requests.post(f"{base_url}/register", json=register_data)
        print(f"📊 Registro - Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Usuario registrado exitosamente")
            result = response.json()
            print(f"🆔 Usuario ID: {result.get('user_id', 'N/A')}")
        elif response.status_code == 400:
            print("⚠️ Usuario ya existe (esto es normal)")
        else:
            print(f"❌ Error: {response.text}")
    
    except Exception as e:
        print(f"❌ Error en registro: {e}")
    
    # Ahora intentemos hacer login
    print("\n2️⃣ Intentando login...")
    
    login_data = {
        "username": "test_user",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{base_url}/login", json=login_data)
        print(f"📊 Login - Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            print("✅ Login exitoso")
            print(f"🔑 Token obtenido: {token[:20]}..." if token else "❌ No token")
        else:
            print(f"❌ Error en login: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
    
    # Verificar el estado general de la API
    print("\n3️⃣ Estado de la API:")
    try:
        response = requests.get(f"{base_url}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data.get('status')}")
            print(f"🗄️ MongoDB: {data.get('mongodb')}")
            
            if data.get('mongodb') == 'connected':
                print("🎉 ¡Base de datos conectada correctamente!")
            else:
                print("❌ Base de datos no conectada")
        else:
            print(f"❌ Error API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error verificando API: {e}")

if __name__ == "__main__":
    check_users()
