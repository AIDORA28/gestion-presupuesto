import requests
import sys
import json
from datetime import datetime

class PersonalFinanceAPITester:
    def __init__(self, base_url="https://credit-simulator-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.user_token = None
        self.admin_token = None
        self.user_id = None
        self.admin_id = None
        self.ingreso_id = None
        self.gasto_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None, token=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        # Add authorization header if token provided
        if token:
            headers['Authorization'] = f'Bearer {token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, params=params)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"   Response: {response.text}")
                except:
                    pass
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test API health check"""
        success, response = self.run_test(
            "API Health Check",
            "GET",
            "",
            200
        )
        return success

    def test_register_regular_user(self):
        """Test regular user registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        user_data = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "email": f"juan.perez.{timestamp}@test.com",
            "telefono": "987654321",
            "dni": f"1234567{timestamp[-2:]}",
            "edad": 30,
            "ocupacion": "Ingeniero",
            "estado_civil": "soltero",
            "dependientes": 1,
            "password": "TestPass123!",
            "is_admin": False
        }
        
        success, response = self.run_test(
            "Register Regular User",
            "POST",
            "register",
            200,
            data=user_data
        )
        
        if success and 'access_token' in response:
            self.user_token = response['access_token']
            self.user_id = response['user']['id']
            print(f"   Created user with ID: {self.user_id}")
            print(f"   Token received: {self.user_token[:20]}...")
            return True
        return False

    def test_register_admin_user(self):
        """Test admin user registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        admin_data = {
            "nombre": "Admin",
            "apellido": "Sistema",
            "email": f"admin.sistema.{timestamp}@test.com",
            "telefono": "987654322",
            "dni": f"8765432{timestamp[-2:]}",
            "edad": 35,
            "ocupacion": "Administrador",
            "estado_civil": "casado",
            "dependientes": 0,
            "password": "AdminPass123!",
            "is_admin": True
        }
        
        success, response = self.run_test(
            "Register Admin User",
            "POST",
            "register",
            200,
            data=admin_data
        )
        
        if success and 'access_token' in response:
            self.admin_token = response['access_token']
            self.admin_id = response['user']['id']
            print(f"   Created admin with ID: {self.admin_id}")
            print(f"   Admin token received: {self.admin_token[:20]}...")
            return True
        return False

    def test_login_user(self):
        """Test user login"""
        # We'll use the registered user's email
        timestamp = datetime.now().strftime('%H%M%S')
        login_data = {
            "email": f"juan.perez.{timestamp}@test.com",
            "password": "TestPass123!"
        }
        
        success, response = self.run_test(
            "User Login",
            "POST",
            "login",
            200,
            data=login_data
        )
        
        if success and 'access_token' in response:
            print(f"   Login successful for user: {response['user']['nombre']}")
            return True
        return False

    def test_get_current_user(self):
        """Test getting current user info"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        success, response = self.run_test(
            "Get Current User Info",
            "GET",
            "me",
            200,
            token=self.user_token
        )
        
        if success and 'id' in response:
            print(f"   User info: {response.get('nombre')} {response.get('apellido')}")
            print(f"   Is Admin: {response.get('is_admin', False)}")
            return True
        return False

    def test_admin_get_users(self):
        """Test admin getting all users"""
        if not self.admin_token:
            print("❌ No admin token available")
            return False
            
        success, response = self.run_test(
            "Admin Get All Users",
            "GET",
            "admin/users",
            200,
            token=self.admin_token
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} users in system")
            return True
        return False

    def test_admin_get_stats(self):
        """Test admin getting system stats"""
        if not self.admin_token:
            print("❌ No admin token available")
            return False
            
        success, response = self.run_test(
            "Admin Get System Stats",
            "GET",
            "admin/stats",
            200,
            token=self.admin_token
        )
        
        if success and 'total_usuarios' in response:
            print(f"   Total usuarios: {response.get('total_usuarios', 0)}")
            print(f"   Total ingresos: {response.get('total_ingresos', 0)}")
            print(f"   Total gastos: {response.get('total_gastos', 0)}")
            print(f"   Total simulaciones: {response.get('total_simulaciones', 0)}")
            return True
        return False

    def test_create_ingreso(self):
        """Test creating income"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        ingreso_data = {
            "tipo": "salario",
            "descripcion": "Salario principal",
            "monto": 3000.00,
            "frecuencia": "mensual",
            "activo": True
        }
        
        success, response = self.run_test(
            "Create Ingreso",
            "POST",
            "ingresos",
            200,
            data=ingreso_data,
            token=self.user_token
        )
        
        if success and 'id' in response:
            self.ingreso_id = response['id']
            print(f"   Created ingreso with ID: {self.ingreso_id}")
            print(f"   Monto: S/ {response.get('monto', 0)}")
            return True
        return False

    def test_get_ingresos(self):
        """Test getting user's income"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        success, response = self.run_test(
            "Get User Ingresos",
            "GET",
            "ingresos",
            200,
            token=self.user_token
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} ingresos")
            return True
        return False

    def test_create_gasto(self):
        """Test creating expense"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        gasto_data = {
            "categoria": "vivienda",
            "descripcion": "Alquiler departamento",
            "monto": 800.00,
            "frecuencia": "mensual",
            "tipo": "fijo",
            "activo": True
        }
        
        success, response = self.run_test(
            "Create Gasto",
            "POST",
            "gastos",
            200,
            data=gasto_data,
            token=self.user_token
        )
        
        if success and 'id' in response:
            self.gasto_id = response['id']
            print(f"   Created gasto with ID: {self.gasto_id}")
            print(f"   Monto: S/ {response.get('monto', 0)}")
            return True
        return False

    def test_get_gastos(self):
        """Test getting user's expenses"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        success, response = self.run_test(
            "Get User Gastos",
            "GET",
            "gastos",
            200,
            token=self.user_token
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} gastos")
            return True
        return False

    def test_flujo_dinero(self):
        """Test cash flow calculation"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        success, response = self.run_test(
            "Calculate Flujo Dinero",
            "GET",
            "flujo-dinero",
            200,
            token=self.user_token
        )
        
        if success and 'ingresos_totales' in response:
            print(f"   Ingresos: S/ {response.get('ingresos_totales', 0)}")
            print(f"   Gastos: S/ {response.get('gastos_totales', 0)}")
            print(f"   Flujo Neto: S/ {response.get('flujo_neto', 0)}")
            print(f"   Ahorro: {response.get('porcentaje_ahorro', 0)}%")
            return True
        return False

    def test_simulacion_credito(self):
        """Test credit simulation"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        simulacion_data = {
            "tipo_credito": "personal",
            "monto_solicitado": 10000.00,
            "plazo_meses": 24
        }
        
        success, response = self.run_test(
            "Create Credit Simulation",
            "POST",
            "simulacion-credito",
            200,
            data=simulacion_data,
            token=self.user_token
        )
        
        if success and 'id' in response:
            print(f"   Score: {response.get('score_crediticio', 0)}")
            print(f"   Aprobado: {response.get('aprobado', False)}")
            print(f"   Cuota: S/ {response.get('cuota_mensual', 0)}")
            return True
        return False

    def test_get_simulaciones(self):
        """Test getting user's simulations"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        success, response = self.run_test(
            "Get User Simulaciones",
            "GET",
            "simulaciones",
            200,
            token=self.user_token
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} simulaciones")
            return True
        return False

    def test_calculo_tributario(self):
        """Test tax calculation - NEW FEATURE"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        success, response = self.run_test(
            "Calculate Tributario",
            "GET",
            "calculo-tributario",
            200,
            token=self.user_token
        )
        
        if success and 'ingresos_anuales' in response:
            print(f"   Ingresos Anuales: S/ {response.get('ingresos_anuales', 0)}")
            print(f"   Base Imponible: S/ {response.get('base_imponible', 0)}")
            print(f"   Impuesto Renta: S/ {response.get('impuesto_renta', 0)}")
            print(f"   Tramo: {response.get('tramo_tributario', 'N/A')}")
            return True
        return False

    def test_sugerencias(self):
        """Test getting financial suggestions"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        success, response = self.run_test(
            "Get Financial Suggestions",
            "GET",
            "sugerencias",
            200,
            token=self.user_token
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} sugerencias")
            for sug in response:
                print(f"     - {sug.get('tipo', 'N/A')}: S/ {sug.get('monto_sugerido', 0)}")
            return True
        return False

    def test_generate_reporte_sunat(self):
        """Test SUNAT report generation"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        success, response = self.run_test(
            "Generate SUNAT Report",
            "POST",
            "reporte-sunat",
            200,
            params={
                "tipo_reporte": "completo",
                "periodo": "2024"
            },
            token=self.user_token
        )
        
        if success and 'id' in response:
            self.reporte_id = response['id']
            print(f"   Generated report with ID: {self.reporte_id}")
            print(f"   Filename: {response.get('nombre_archivo', 'N/A')}")
            return True
        return False

    def test_get_reportes_sunat(self):
        """Test getting SUNAT reports"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        success, response = self.run_test(
            "Get SUNAT Reports",
            "GET",
            "reportes-sunat",
            200,
            token=self.user_token
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} reportes")
            return True
        return False

    def test_download_reporte(self):
        """Test downloading SUNAT report"""
        if not self.user_token or not hasattr(self, 'reporte_id'):
            print("❌ No user token or report ID available")
            return False
            
        success, response = self.run_test(
            "Download SUNAT Report",
            "GET",
            f"reportes-sunat/{self.reporte_id}/download",
            200,
            token=self.user_token
        )
        
        return success

    def test_unauthorized_access(self):
        """Test that protected endpoints require authentication"""
        success, response = self.run_test(
            "Unauthorized Access Test",
            "GET",
            "me",
            401  # Should return 401 Unauthorized
        )
        
        if success:
            print("   ✅ Properly blocked unauthorized access")
            return True
        return False

    def test_regular_user_admin_access(self):
        """Test that regular users cannot access admin endpoints"""
        if not self.user_token:
            print("❌ No user token available")
            return False
            
        success, response = self.run_test(
            "Regular User Admin Access Test",
            "GET",
            "admin/users",
            403,  # Should return 403 Forbidden
            token=self.user_token
        )
        
        if success:
            print("   ✅ Properly blocked regular user from admin endpoints")
            return True
        return False

    def test_delete_operations(self):
        """Test delete operations"""
        success_count = 0
        
        # Delete ingreso
        if self.ingreso_id and self.user_token:
            success, _ = self.run_test(
                "Delete Ingreso",
                "DELETE",
                f"ingresos/{self.ingreso_id}",
                200,
                token=self.user_token
            )
            if success:
                success_count += 1
        
        # Delete gasto
        if self.gasto_id and self.user_token:
            success, _ = self.run_test(
                "Delete Gasto",
                "DELETE",
                f"gastos/{self.gasto_id}",
                200,
                token=self.user_token
            )
            if success:
                success_count += 1
                
        return success_count > 0

def main():
    print("🚀 Starting Personal Finance API Tests")
    print("=" * 60)
    
    tester = PersonalFinanceAPITester()
    
    # Run all tests in sequence
    test_methods = [
        # Basic API tests
        tester.test_health_check,
        
        # Authentication tests
        tester.test_register_regular_user,
        tester.test_register_admin_user,
        tester.test_login_user,
        tester.test_get_current_user,
        
        # Admin functionality tests
        tester.test_admin_get_users,
        tester.test_admin_get_stats,
        
        # Financial data tests
        tester.test_create_ingreso,
        tester.test_get_ingresos,
        tester.test_create_gasto,
        tester.test_get_gastos,
        tester.test_flujo_dinero,
        
        # Credit simulation tests
        tester.test_simulacion_credito,
        tester.test_get_simulaciones,
        
        # NEW: Tax calculation tests
        tester.test_calculo_tributario,
        
        # Suggestions tests
        tester.test_sugerencias,
        
        # Report generation tests
        tester.test_generate_reporte_sunat,
        tester.test_get_reportes_sunat,
        tester.test_download_reporte,
        
        # Security tests
        tester.test_unauthorized_access,
        tester.test_regular_user_admin_access,
        
        # Cleanup tests
        tester.test_delete_operations
    ]
    
    for test_method in test_methods:
        try:
            test_method()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {tester.tests_run - tester.tests_passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())