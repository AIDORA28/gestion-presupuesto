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

    def test_create_user(self):
        """Test user creation"""
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
            "dependientes": 1
        }
        
        success, response = self.run_test(
            "Create User",
            "POST",
            "users",
            200,
            data=user_data
        )
        
        if success and 'id' in response:
            self.user_id = response['id']
            print(f"   Created user with ID: {self.user_id}")
            return True
        return False

    def test_get_users(self):
        """Test getting all users"""
        success, response = self.run_test(
            "Get All Users",
            "GET",
            "users",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} users")
            return True
        return False

    def test_get_user_by_id(self):
        """Test getting user by ID"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
            
        success, response = self.run_test(
            "Get User by ID",
            "GET",
            f"users/{self.user_id}",
            200
        )
        
        if success and response.get('id') == self.user_id:
            print(f"   Retrieved user: {response.get('nombre')} {response.get('apellido')}")
            return True
        return False

    def test_create_ingreso(self):
        """Test creating income"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
            
        ingreso_data = {
            "user_id": self.user_id,
            "tipo": "salario",
            "descripcion": "Salario principal",
            "monto": 3000.00,
            "frecuencia": "mensual"
        }
        
        success, response = self.run_test(
            "Create Ingreso",
            "POST",
            "ingresos",
            200,
            data=ingreso_data
        )
        
        if success and 'id' in response:
            self.ingreso_id = response['id']
            print(f"   Created ingreso with ID: {self.ingreso_id}")
            return True
        return False

    def test_get_ingresos(self):
        """Test getting user's income"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
            
        success, response = self.run_test(
            "Get User Ingresos",
            "GET",
            f"ingresos/{self.user_id}",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} ingresos")
            return True
        return False

    def test_create_gasto(self):
        """Test creating expense"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
            
        gasto_data = {
            "user_id": self.user_id,
            "categoria": "vivienda",
            "descripcion": "Alquiler departamento",
            "monto": 800.00,
            "frecuencia": "mensual",
            "tipo": "fijo"
        }
        
        success, response = self.run_test(
            "Create Gasto",
            "POST",
            "gastos",
            200,
            data=gasto_data
        )
        
        if success and 'id' in response:
            self.gasto_id = response['id']
            print(f"   Created gasto with ID: {self.gasto_id}")
            return True
        return False

    def test_get_gastos(self):
        """Test getting user's expenses"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
            
        success, response = self.run_test(
            "Get User Gastos",
            "GET",
            f"gastos/{self.user_id}",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} gastos")
            return True
        return False

    def test_flujo_dinero(self):
        """Test cash flow calculation"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
            
        success, response = self.run_test(
            "Calculate Flujo Dinero",
            "GET",
            f"flujo-dinero/{self.user_id}",
            200
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
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
            
        simulacion_data = {
            "user_id": self.user_id,
            "tipo_credito": "personal",
            "monto_solicitado": 10000.00,
            "plazo_meses": 24
        }
        
        success, response = self.run_test(
            "Create Credit Simulation",
            "POST",
            "simulacion-credito",
            200,
            data=simulacion_data
        )
        
        if success and 'id' in response:
            print(f"   Score: {response.get('score_crediticio', 0)}")
            print(f"   Aprobado: {response.get('aprobado', False)}")
            print(f"   Cuota: S/ {response.get('cuota_mensual', 0)}")
            return True
        return False

    def test_get_simulaciones(self):
        """Test getting user's simulations"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
            
        success, response = self.run_test(
            "Get User Simulaciones",
            "GET",
            f"simulaciones/{self.user_id}",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} simulaciones")
            return True
        return False

    def test_sugerencias(self):
        """Test getting financial suggestions"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
            
        success, response = self.run_test(
            "Get Financial Suggestions",
            "GET",
            f"sugerencias/{self.user_id}",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} sugerencias")
            for sug in response:
                print(f"     - {sug.get('tipo', 'N/A')}: {sug.get('descripcion', 'N/A')}")
            return True
        return False

    def test_generate_reporte_sunat(self):
        """Test SUNAT report generation"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
            
        success, response = self.run_test(
            "Generate SUNAT Report",
            "POST",
            "reporte-sunat",
            200,
            params={
                "user_id": self.user_id,
                "tipo_reporte": "completo",
                "periodo": "2024"
            }
        )
        
        if success and 'id' in response:
            print(f"   Generated report with ID: {response['id']}")
            return True
        return False

    def test_get_reportes_sunat(self):
        """Test getting SUNAT reports"""
        if not self.user_id:
            print("❌ No user ID available for testing")
            return False
            
        success, response = self.run_test(
            "Get SUNAT Reports",
            "GET",
            f"reportes-sunat/{self.user_id}",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} reportes")
            return True
        return False

    def test_delete_operations(self):
        """Test delete operations"""
        success_count = 0
        
        # Delete ingreso
        if hasattr(self, 'ingreso_id'):
            success, _ = self.run_test(
                "Delete Ingreso",
                "DELETE",
                f"ingresos/{self.ingreso_id}",
                200
            )
            if success:
                success_count += 1
        
        # Delete gasto
        if hasattr(self, 'gasto_id'):
            success, _ = self.run_test(
                "Delete Gasto",
                "DELETE",
                f"gastos/{self.gasto_id}",
                200
            )
            if success:
                success_count += 1
                
        return success_count > 0

def main():
    print("🚀 Starting Personal Finance API Tests")
    print("=" * 50)
    
    tester = PersonalFinanceAPITester()
    
    # Run all tests in sequence
    test_methods = [
        tester.test_health_check,
        tester.test_create_user,
        tester.test_get_users,
        tester.test_get_user_by_id,
        tester.test_create_ingreso,
        tester.test_get_ingresos,
        tester.test_create_gasto,
        tester.test_get_gastos,
        tester.test_flujo_dinero,
        tester.test_simulacion_credito,
        tester.test_get_simulaciones,
        tester.test_sugerencias,
        tester.test_generate_reporte_sunat,
        tester.test_get_reportes_sunat,
        tester.test_delete_operations
    ]
    
    for test_method in test_methods:
        try:
            test_method()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {tester.tests_run - tester.tests_passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())