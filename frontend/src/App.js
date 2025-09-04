import React, { useState, useEffect, useContext, createContext } from "react";
import "./App.css";
import axios from "axios";
import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom";
import { Button } from "./components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Badge } from "./components/ui/badge";
import { Separator } from "./components/ui/separator";
import { Alert, AlertDescription } from "./components/ui/alert";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "./components/ui/dialog";
import { Textarea } from "./components/ui/textarea";
import { toast } from "sonner";
import { Toaster } from "./components/ui/sonner";
import { 
  User, 
  DollarSign, 
  TrendingUp, 
  CreditCard, 
  FileText, 
  PlusCircle, 
  Trash2,
  Calculator,
  PieChart,
  BarChart3,
  CheckCircle,
  XCircle,
  Lightbulb,
  Download,
  Shield,
  Users,
  LogOut,
  Eye,
  Receipt,
  TrendingDown,
  Building2
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Context para autenticación
const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchCurrentUser = async () => {
    try {
      const response = await axios.get(`${API}/me`);
      setUser(response.data);
    } catch (error) {
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = (userData, accessToken) => {
    setUser(userData);
    setToken(accessToken);
    localStorage.setItem('token', accessToken);
    axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de AuthProvider');
  }
  return context;
};

// Componente de Login
const LoginForm = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    nombre: '',
    apellido: '',
    telefono: '',
    dni: '',
    edad: '',
    ocupacion: '',
    estado_civil: '',
    dependientes: 0,
    is_admin: false
  });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let response;
      if (isLogin) {
        response = await axios.post(`${API}/login`, {
          email: formData.email,
          password: formData.password
        });
      } else {
        response = await axios.post(`${API}/register`, {
          ...formData,
          edad: parseInt(formData.edad),
          dependientes: parseInt(formData.dependientes)
        });
      }

      login(response.data.user, response.data.access_token);
      toast.success(isLogin ? 'Bienvenido' : 'Cuenta creada exitosamente');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error en la autenticación');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 to-cyan-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl shadow-2xl border-0 bg-white/90 backdrop-blur-sm">
        <CardHeader className="text-center pb-8">
          <div className="w-20 h-20 bg-gradient-to-br from-sky-400 to-cyan-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
            <DollarSign className="w-10 h-10 text-white" />
          </div>
          <CardTitle className="text-3xl font-bold text-slate-800 mb-2">
            Finanzas Personales
          </CardTitle>
          <CardDescription className="text-lg text-slate-600">
            {isLogin ? 'Ingresa a tu cuenta' : 'Crea tu cuenta nueva'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {!isLogin && (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="nombre">Nombre</Label>
                    <Input
                      id="nombre"
                      value={formData.nombre}
                      onChange={(e) => setFormData({...formData, nombre: e.target.value})}
                      required={!isLogin}
                      className="border-sky-200 focus:border-sky-400"
                    />
                  </div>
                  <div>
                    <Label htmlFor="apellido">Apellido</Label>
                    <Input
                      id="apellido"
                      value={formData.apellido}
                      onChange={(e) => setFormData({...formData, apellido: e.target.value})}
                      required={!isLogin}
                      className="border-sky-200 focus:border-sky-400"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="telefono">Teléfono</Label>
                    <Input
                      id="telefono"
                      value={formData.telefono}
                      onChange={(e) => setFormData({...formData, telefono: e.target.value})}
                      required={!isLogin}
                      className="border-sky-200 focus:border-sky-400"
                    />
                  </div>
                  <div>
                    <Label htmlFor="dni">DNI</Label>
                    <Input
                      id="dni"
                      value={formData.dni}
                      onChange={(e) => setFormData({...formData, dni: e.target.value})}
                      required={!isLogin}
                      className="border-sky-200 focus:border-sky-400"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="edad">Edad</Label>
                    <Input
                      id="edad"
                      type="number"
                      value={formData.edad}
                      onChange={(e) => setFormData({...formData, edad: e.target.value})}
                      required={!isLogin}
                      className="border-sky-200 focus:border-sky-400"
                    />
                  </div>
                  <div>
                    <Label htmlFor="dependientes">Dependientes</Label>
                    <Input
                      id="dependientes"
                      type="number"
                      value={formData.dependientes}
                      onChange={(e) => setFormData({...formData, dependientes: e.target.value})}
                      className="border-sky-200 focus:border-sky-400"
                    />
                  </div>
                  <div className="flex items-center space-x-2 pt-6">
                    <input
                      type="checkbox"
                      id="is_admin"
                      checked={formData.is_admin}
                      onChange={(e) => setFormData({...formData, is_admin: e.target.checked})}
                      className="w-4 h-4 text-sky-600"
                    />
                    <Label htmlFor="is_admin" className="text-sm">Administrador</Label>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="ocupacion">Ocupación</Label>
                    <Input
                      id="ocupacion"
                      value={formData.ocupacion}
                      onChange={(e) => setFormData({...formData, ocupacion: e.target.value})}
                      required={!isLogin}
                      className="border-sky-200 focus:border-sky-400"
                    />
                  </div>
                  <div>
                    <Label htmlFor="estado_civil">Estado Civil</Label>
                    <Select 
                      value={formData.estado_civil} 
                      onValueChange={(value) => setFormData({...formData, estado_civil: value})}
                    >
                      <SelectTrigger className="border-sky-200 focus:border-sky-400">
                        <SelectValue placeholder="Selecciona tu estado civil" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="soltero">Soltero/a</SelectItem>
                        <SelectItem value="casado">Casado/a</SelectItem>
                        <SelectItem value="divorciado">Divorciado/a</SelectItem>
                        <SelectItem value="viudo">Viudo/a</SelectItem>
                        <SelectItem value="union_libre">Unión Libre</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </>
            )}

            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
                className="border-sky-200 focus:border-sky-400"
              />
            </div>

            <div>
              <Label htmlFor="password">Contraseña</Label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
                className="border-sky-200 focus:border-sky-400"
              />
            </div>

            <Button 
              type="submit" 
              className="w-full bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600 text-white font-semibold py-3 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300" 
              disabled={loading}
            >
              {loading ? 'Procesando...' : isLogin ? 'Iniciar Sesión' : 'Crear Cuenta'}
            </Button>

            <div className="text-center">
              <Button
                type="button"
                variant="ghost"
                onClick={() => setIsLogin(!isLogin)}
                className="text-sky-600 hover:text-sky-800"
              >
                {isLogin ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Inicia sesión'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

// Header con información del usuario
const Header = () => {
  const { user, logout } = useAuth();

  return (
    <div className="bg-white shadow-sm border-b border-sky-100 mb-8">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-br from-sky-400 to-cyan-500 rounded-full flex items-center justify-center">
              <DollarSign className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-800">Finanzas Personales</h1>
              <p className="text-slate-600">Bienvenido, {user?.nombre} {user?.apellido}</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            {user?.is_admin && (
              <Badge className="bg-gradient-to-r from-amber-400 to-orange-500 text-white">
                <Shield className="w-3 h-3 mr-1" />
                Administrador
              </Badge>
            )}
            <Button variant="outline" onClick={logout} className="border-sky-200 hover:bg-sky-50">
              <LogOut className="w-4 h-4 mr-2" />
              Cerrar Sesión
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Dashboard principal
const Dashboard = () => {
  const { user } = useAuth();
  const [flujoDinero, setFlujoDinero] = useState(null);
  const [ingresos, setIngresos] = useState([]);
  const [gastos, setGastos] = useState([]);
  const [simulaciones, setSimulaciones] = useState([]);
  const [sugerencias, setSugerencias] = useState([]);
  const [calculoTributario, setCalculoTributario] = useState(null);

  useEffect(() => {
    if (user) {
      fetchFlujoDinero();
      fetchIngresos();
      fetchGastos();
      fetchSimulaciones();
      fetchSugerencias();
      fetchCalculoTributario();
    }
  }, [user]);

  const fetchFlujoDinero = async () => {
    try {
      const response = await axios.get(`${API}/flujo-dinero`);
      setFlujoDinero(response.data);
    } catch (error) {
      console.error('Error fetching flujo dinero:', error);
    }
  };

  const fetchIngresos = async () => {
    try {
      const response = await axios.get(`${API}/ingresos`);
      setIngresos(response.data);
    } catch (error) {
      console.error('Error fetching ingresos:', error);
    }
  };

  const fetchGastos = async () => {
    try {
      const response = await axios.get(`${API}/gastos`);
      setGastos(response.data);
    } catch (error) {
      console.error('Error fetching gastos:', error);
    }
  };

  const fetchSimulaciones = async () => {
    try {
      const response = await axios.get(`${API}/simulaciones`);
      setSimulaciones(response.data);
    } catch (error) {
      console.error('Error fetching simulaciones:', error);
    }
  };

  const fetchSugerencias = async () => {
    try {
      const response = await axios.get(`${API}/sugerencias`);
      setSugerencias(response.data);
    } catch (error) {
      console.error('Error fetching sugerencias:', error);
    }
  };

  const fetchCalculoTributario = async () => {
    try {
      const response = await axios.get(`${API}/calculo-tributario`);
      setCalculoTributario(response.data);
    } catch (error) {
      console.error('Error fetching calculo tributario:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 to-cyan-50">
      <Header />
      <div className="container mx-auto px-4 pb-8">
        {/* Resumen financiero */}
        {flujoDinero && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <StatsCard
              title="Ingresos Totales"
              value={`S/ ${flujoDinero.ingresos_totales?.toFixed(2) || '0.00'}`}
              icon={<TrendingUp className="w-6 h-6 text-emerald-600" />}
              bgColor="bg-gradient-to-br from-emerald-50 to-green-100"
            />
            <StatsCard
              title="Gastos Totales"
              value={`S/ ${flujoDinero.gastos_totales?.toFixed(2) || '0.00'}`}
              icon={<TrendingDown className="w-6 h-6 text-rose-600" />}
              bgColor="bg-gradient-to-br from-rose-50 to-red-100"
            />
            <StatsCard
              title="Flujo Neto"
              value={`S/ ${flujoDinero.flujo_neto?.toFixed(2) || '0.00'}`}
              icon={<BarChart3 className="w-6 h-6 text-sky-600" />}
              bgColor="bg-gradient-to-br from-sky-50 to-blue-100"
            />
            <StatsCard
              title="Capacidad de Ahorro"
              value={`${flujoDinero.porcentaje_ahorro?.toFixed(1) || '0.0'}%`}
              icon={<PieChart className="w-6 h-6 text-violet-600" />}
              bgColor="bg-gradient-to-br from-violet-50 to-purple-100"
            />
          </div>
        )}

        {/* Tabs principales */}
        <Tabs defaultValue="ingresos" className="space-y-6">
          <TabsList className="grid grid-cols-6 w-full bg-white shadow-sm border border-sky-100">
            <TabsTrigger value="ingresos" className="data-[state=active]:bg-sky-100 data-[state=active]:text-sky-800">Ingresos</TabsTrigger>
            <TabsTrigger value="gastos" className="data-[state=active]:bg-sky-100 data-[state=active]:text-sky-800">Gastos</TabsTrigger>
            <TabsTrigger value="credito" className="data-[state=active]:bg-sky-100 data-[state=active]:text-sky-800">Simulador</TabsTrigger>
            <TabsTrigger value="tributario" className="data-[state=active]:bg-sky-100 data-[state=active]:text-sky-800">Tributario</TabsTrigger>
            <TabsTrigger value="sugerencias" className="data-[state=active]:bg-sky-100 data-[state=active]:text-sky-800">Sugerencias</TabsTrigger>
            <TabsTrigger value="reportes" className="data-[state=active]:bg-sky-100 data-[state=active]:text-sky-800">Reportes</TabsTrigger>
            {user?.is_admin && (
              <TabsTrigger value="admin" className="data-[state=active]:bg-amber-100 data-[state=active]:text-amber-800">Admin</TabsTrigger>
            )}
          </TabsList>

          <TabsContent value="ingresos">
            <IngresosSection 
              ingresos={ingresos} 
              onUpdate={fetchIngresos}
              onFlowUpdate={fetchFlujoDinero}
            />
          </TabsContent>

          <TabsContent value="gastos">
            <GastosSection 
              gastos={gastos} 
              onUpdate={fetchGastos}
              onFlowUpdate={fetchFlujoDinero}
            />
          </TabsContent>

          <TabsContent value="credito">
            <CreditoSection 
              simulaciones={simulaciones}
              onUpdate={fetchSimulaciones}
            />
          </TabsContent>

          <TabsContent value="tributario">
            <TributarioSection 
              calculoTributario={calculoTributario}
              onUpdate={fetchCalculoTributario}
            />
          </TabsContent>

          <TabsContent value="sugerencias">
            <SugerenciasSection sugerencias={sugerencias} />
          </TabsContent>

          <TabsContent value="reportes">
            <ReportesSection />
          </TabsContent>

          {user?.is_admin && (
            <TabsContent value="admin">
              <AdminSection />
            </TabsContent>
          )}
        </Tabs>
      </div>
      <Toaster />
    </div>
  );
};

// Componente de estadísticas
const StatsCard = ({ title, value, icon, bgColor }) => (
  <Card className={`${bgColor} border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105`}>
    <CardContent className="p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-slate-600">{title}</p>
          <p className="text-2xl font-bold text-slate-800">{value}</p>
        </div>
        {icon}
      </div>
    </CardContent>
  </Card>
);

// Sección de Ingresos
const IngresosSection = ({ ingresos, onUpdate, onFlowUpdate }) => {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    tipo: '',
    descripcion: '',
    monto: '',
    frecuencia: 'mensual'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/ingresos`, {
        ...formData,
        monto: parseFloat(formData.monto)
      });
      toast.success('Ingreso agregado exitosamente');
      setFormData({ tipo: '', descripcion: '', monto: '', frecuencia: 'mensual' });
      setShowForm(false);
      onUpdate();
      onFlowUpdate();
    } catch (error) {
      toast.error('Error al agregar ingreso');
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API}/ingresos/${id}`);
      toast.success('Ingreso eliminado');
      onUpdate();
      onFlowUpdate();
    } catch (error) {
      toast.error('Error al eliminar ingreso');
    }
  };

  return (
    <Card className="shadow-lg border-sky-100">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span className="flex items-center gap-2 text-sky-800">
            <TrendingUp className="w-5 h-5" />
            Gestión de Ingresos
          </span>
          <Button onClick={() => setShowForm(true)} className="bg-gradient-to-r from-emerald-500 to-green-500 hover:from-emerald-600 hover:to-green-600">
            <PlusCircle className="w-4 h-4 mr-2" />
            Agregar Ingreso
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {showForm && (
          <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded-lg bg-sky-50/50">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label>Tipo de Ingreso</Label>
                <Select value={formData.tipo} onValueChange={(value) => setFormData({...formData, tipo: value})}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecciona el tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="salario">Salario</SelectItem>
                    <SelectItem value="freelance">Freelance</SelectItem>
                    <SelectItem value="inversion">Inversión</SelectItem>
                    <SelectItem value="negocio">Negocio Propio</SelectItem>
                    <SelectItem value="otro">Otro</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Frecuencia</Label>
                <Select value={formData.frecuencia} onValueChange={(value) => setFormData({...formData, frecuencia: value})}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="semanal">Semanal</SelectItem>
                    <SelectItem value="quincenal">Quincenal</SelectItem>
                    <SelectItem value="mensual">Mensual</SelectItem>
                    <SelectItem value="anual">Anual</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div>
              <Label>Descripción</Label>
              <Input
                value={formData.descripcion}
                onChange={(e) => setFormData({...formData, descripcion: e.target.value})}
                placeholder="Ej: Salario trabajo principal"
                required
              />
            </div>
            <div>
              <Label>Monto (S/)</Label>
              <Input
                type="number"
                step="0.01"
                value={formData.monto}
                onChange={(e) => setFormData({...formData, monto: e.target.value})}
                required
              />
            </div>
            <div className="flex gap-2">
              <Button type="submit" className="bg-emerald-600 hover:bg-emerald-700">Guardar</Button>
              <Button type="button" variant="outline" onClick={() => setShowForm(false)}>Cancelar</Button>
            </div>
          </form>
        )}

        <div className="space-y-3">
          {ingresos.map(ingreso => (
            <div key={ingreso.id} className="flex items-center justify-between p-4 border rounded-lg bg-white shadow-sm hover:shadow-md transition-shadow">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <Badge className="bg-emerald-100 text-emerald-800">{ingreso.tipo}</Badge>
                  <Badge variant="outline">{ingreso.frecuencia}</Badge>
                </div>
                <p className="font-medium">{ingreso.descripcion}</p>
                <p className="text-2xl font-bold text-emerald-600">S/ {ingreso.monto.toFixed(2)}</p>
              </div>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => handleDelete(ingreso.id)}
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
          ))}
          {ingresos.length === 0 && (
            <p className="text-center text-slate-500 py-8">No tienes ingresos registrados</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

// Sección de Gastos
const GastosSection = ({ gastos, onUpdate, onFlowUpdate }) => {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    categoria: '',
    descripcion: '',
    monto: '',
    frecuencia: 'mensual',
    tipo: 'fijo'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/gastos`, {
        ...formData,
        monto: parseFloat(formData.monto)
      });
      toast.success('Gasto agregado exitosamente');
      setFormData({ categoria: '', descripcion: '', monto: '', frecuencia: 'mensual', tipo: 'fijo' });
      setShowForm(false);
      onUpdate();
      onFlowUpdate();
    } catch (error) {
      toast.error('Error al agregar gasto');
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API}/gastos/${id}`);
      toast.success('Gasto eliminado');
      onUpdate();
      onFlowUpdate();
    } catch (error) {
      toast.error('Error al eliminar gasto');
    }
  };

  return (
    <Card className="shadow-lg border-sky-100">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span className="flex items-center gap-2 text-sky-800">
            <TrendingDown className="w-5 h-5" />
            Gestión de Gastos
          </span>
          <Button onClick={() => setShowForm(true)} className="bg-gradient-to-r from-rose-500 to-red-500 hover:from-rose-600 hover:to-red-600">
            <PlusCircle className="w-4 h-4 mr-2" />
            Agregar Gasto
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {showForm && (
          <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded-lg bg-sky-50/50">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <Label>Categoría</Label>
                <Select value={formData.categoria} onValueChange={(value) => setFormData({...formData, categoria: value})}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecciona categoría" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="vivienda">Vivienda</SelectItem>
                    <SelectItem value="alimentacion">Alimentación</SelectItem>
                    <SelectItem value="transporte">Transporte</SelectItem>
                    <SelectItem value="salud">Salud</SelectItem>
                    <SelectItem value="educacion">Educación</SelectItem>
                    <SelectItem value="entretenimiento">Entretenimiento</SelectItem>
                    <SelectItem value="otros">Otros</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Tipo</Label>
                <Select value={formData.tipo} onValueChange={(value) => setFormData({...formData, tipo: value})}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="fijo">Fijo</SelectItem>
                    <SelectItem value="variable">Variable</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Frecuencia</Label>
                <Select value={formData.frecuencia} onValueChange={(value) => setFormData({...formData, frecuencia: value})}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="semanal">Semanal</SelectItem>
                    <SelectItem value="quincenal">Quincenal</SelectItem>
                    <SelectItem value="mensual">Mensual</SelectItem>
                    <SelectItem value="anual">Anual</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div>
              <Label>Descripción</Label>
              <Input
                value={formData.descripcion}
                onChange={(e) => setFormData({...formData, descripcion: e.target.value})}
                placeholder="Ej: Alquiler departamento"
                required
              />
            </div>
            <div>
              <Label>Monto (S/)</Label>
              <Input
                type="number"
                step="0.01"
                value={formData.monto}
                onChange={(e) => setFormData({...formData, monto: e.target.value})}
                required
              />
            </div>
            <div className="flex gap-2">
              <Button type="submit" className="bg-rose-600 hover:bg-rose-700">Guardar</Button>
              <Button type="button" variant="outline" onClick={() => setShowForm(false)}>Cancelar</Button>
            </div>
          </form>
        )}

        <div className="space-y-3">
          {gastos.map(gasto => (
            <div key={gasto.id} className="flex items-center justify-between p-4 border rounded-lg bg-white shadow-sm hover:shadow-md transition-shadow">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <Badge className="bg-rose-100 text-rose-800">{gasto.categoria}</Badge>
                  <Badge variant="outline">{gasto.tipo}</Badge>
                  <Badge variant="outline">{gasto.frecuencia}</Badge>
                </div>
                <p className="font-medium">{gasto.descripcion}</p>
                <p className="text-2xl font-bold text-rose-600">S/ {gasto.monto.toFixed(2)}</p>
              </div>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => handleDelete(gasto.id)}
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
          ))}
          {gastos.length === 0 && (
            <p className="text-center text-slate-500 py-8">No tienes gastos registrados</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

// Sección de Simulador de Crédito
const CreditoSection = ({ simulaciones, onUpdate }) => {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    tipo_credito: '',
    monto_solicitado: '',
    plazo_meses: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await axios.post(`${API}/simulacion-credito`, {
        ...formData,
        monto_solicitado: parseFloat(formData.monto_solicitado),
        plazo_meses: parseInt(formData.plazo_meses)
      });
      toast.success('Simulación realizada exitosamente');
      setFormData({ tipo_credito: '', monto_solicitado: '', plazo_meses: '' });
      setShowForm(false);
      onUpdate();
    } catch (error) {
      toast.error('Error al realizar simulación');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="shadow-lg border-sky-100">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span className="flex items-center gap-2 text-sky-800">
            <Calculator className="w-5 h-5" />
            Simulador de Crédito
          </span>
          <Button onClick={() => setShowForm(true)} className="bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600">
            <PlusCircle className="w-4 h-4 mr-2" />
            Nueva Simulación
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {showForm && (
          <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded-lg bg-sky-50/50">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <Label>Tipo de Crédito</Label>
                <Select value={formData.tipo_credito} onValueChange={(value) => setFormData({...formData, tipo_credito: value})}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecciona el tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="personal">Personal</SelectItem>
                    <SelectItem value="hipotecario">Hipotecario</SelectItem>
                    <SelectItem value="vehicular">Vehicular</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Monto Solicitado (S/)</Label>
                <Input
                  type="number"
                  step="0.01"
                  value={formData.monto_solicitado}
                  onChange={(e) => setFormData({...formData, monto_solicitado: e.target.value})}
                  required
                />
              </div>
              <div>
                <Label>Plazo (meses)</Label>
                <Input
                  type="number"
                  value={formData.plazo_meses}
                  onChange={(e) => setFormData({...formData, plazo_meses: e.target.value})}
                  required
                />
              </div>
            </div>
            <div className="flex gap-2">
              <Button type="submit" className="bg-sky-600 hover:bg-sky-700" disabled={loading}>
                {loading ? 'Simulando...' : 'Simular Crédito'}
              </Button>
              <Button type="button" variant="outline" onClick={() => setShowForm(false)}>Cancelar</Button>
            </div>
          </form>
        )}

        <div className="space-y-4">
          {simulaciones.map(sim => (
            <Card key={sim.id} className={`${sim.aprobado ? 'border-emerald-500 bg-emerald-50/30' : 'border-rose-500 bg-rose-50/30'} border-2`}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <Badge className="bg-sky-100 text-sky-800">{sim.tipo_credito}</Badge>
                    {sim.aprobado ? (
                      <Badge className="bg-emerald-100 text-emerald-800">
                        <CheckCircle className="w-3 h-3 mr-1" />
                        Pre-aprobado
                      </Badge>
                    ) : (
                      <Badge className="bg-rose-100 text-rose-800">
                        <XCircle className="w-3 h-3 mr-1" />
                        No aprobado
                      </Badge>
                    )}
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-slate-600">Score Crediticio</p>
                    <p className="text-2xl font-bold">{sim.score_crediticio.toFixed(0)}</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-slate-600">Monto Solicitado</p>
                    <p className="text-lg font-semibold">S/ {sim.monto_solicitado.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-600">Cuota Mensual</p>
                    <p className="text-lg font-semibold">S/ {sim.cuota_mensual.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-600">Total a Pagar</p>
                    <p className="text-lg font-semibold">S/ {sim.total_pagar.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-600">Tasa de Interés</p>
                    <p className="text-lg font-semibold">{sim.tasa_interes}% anual</p>
                  </div>
                </div>
                
                <Separator className="my-4" />
                
                <div>
                  <p className="text-sm text-slate-600 mb-2">Observaciones</p>
                  <p className="text-sm">{sim.observaciones}</p>
                </div>
              </CardContent>
            </Card>
          ))}
          {simulaciones.length === 0 && (
            <p className="text-center text-slate-500 py-8">No tienes simulaciones realizadas</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

// Nueva Sección Tributaria
const TributarioSection = ({ calculoTributario, onUpdate }) => {
  const [loading, setLoading] = useState(false);

  const recalcularTributario = async () => {
    setLoading(true);
    try {
      await onUpdate();
      toast.success('Cálculo tributario actualizado');
    } catch (error) {
      toast.error('Error al calcular tributario');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="shadow-lg border-sky-100">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span className="flex items-center gap-2 text-sky-800">
            <Building2 className="w-5 h-5" />
            Cálculo Tributario y Renta
          </span>
          <Button onClick={recalcularTributario} disabled={loading} className="bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600">
            <Calculator className="w-4 h-4 mr-2" />
            {loading ? 'Calculando...' : 'Recalcular'}
          </Button>
        </CardTitle>
        <CardDescription>
          Cálculo del impuesto a la renta basado en tus ingresos y gastos actuales
        </CardDescription>
      </CardHeader>
      <CardContent>
        {calculoTributario ? (
          <div className="space-y-6">
            {/* Resumen tributario */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="bg-gradient-to-br from-sky-50 to-cyan-50 border-sky-200">
                <CardContent className="p-6">
                  <h3 className="font-semibold text-lg mb-4 text-sky-800">Resumen Anual</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-slate-600">Ingresos Anuales:</span>
                      <span className="font-semibold">S/ {calculoTributario.ingresos_anuales.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-600">Gastos Deducibles:</span>
                      <span className="font-semibold">S/ {calculoTributario.gastos_deducibles.toFixed(2)}</span>
                    </div>
                    <Separator />
                    <div className="flex justify-between">
                      <span className="text-slate-600">Base Imponible:</span>
                      <span className="font-semibold">S/ {calculoTributario.base_imponible.toFixed(2)}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-amber-50 to-orange-50 border-amber-200">
                <CardContent className="p-6">
                  <h3 className="font-semibold text-lg mb-4 text-amber-800">Impuesto a Pagar</h3>
                  <div className="space-y-3">
                    <div className="text-center">
                      <p className="text-3xl font-bold text-amber-800">
                        S/ {calculoTributario.impuesto_renta.toFixed(2)}
                      </p>
                      <p className="text-sm text-slate-600">Impuesto anual</p>
                    </div>
                    <Separator />
                    <div className="flex justify-between">
                      <span className="text-slate-600">Tasa aplicada:</span>
                      <span className="font-semibold">{calculoTributario.porcentaje_impuesto}%</span>
                    </div>
                    <div className="text-center">
                      <Badge className="bg-amber-100 text-amber-800">
                        {calculoTributario.tramo_tributario}
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Información adicional */}
            <Card className="bg-gradient-to-br from-slate-50 to-gray-50 border-slate-200">
              <CardContent className="p-6">
                <h3 className="font-semibold text-lg mb-4 text-slate-800">Información Tributaria 2024</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium mb-2">Tramos del Impuesto a la Renta:</h4>
                    <ul className="text-sm space-y-1 text-slate-600">
                      <li>• Hasta 5 UIT (S/ 25,750): Exonerado</li>
                      <li>• De 5 a 20 UIT: 8%</li>
                      <li>• De 20 a 35 UIT: 14%</li>
                      <li>• De 35 a 45 UIT: 17%</li>
                      <li>• Más de 45 UIT: 30%</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Recomendaciones:</h4>
                    <ul className="text-sm space-y-1 text-slate-600">
                      <li>• Conserva todos tus recibos deducibles</li>
                      <li>• Considera aportes voluntarios al SPP</li>
                      <li>• Declara antes del 31 de marzo</li>
                      <li>• Consulta con un contador especializado</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Proyección mensual */}
            <Alert className="border-sky-200 bg-sky-50">
              <Receipt className="h-4 w-4" />
              <AlertDescription>
                <strong>Proyección mensual:</strong> Basado en tu cálculo anual, deberías apartar aproximadamente 
                <strong> S/ {(calculoTributario.impuesto_renta / 12).toFixed(2)}</strong> mensuales para el pago del impuesto a la renta.
              </AlertDescription>
            </Alert>
          </div>
        ) : (
          <div className="text-center py-8">
            <Receipt className="w-16 h-16 text-slate-400 mx-auto mb-4" />
            <p className="text-slate-500">No hay datos suficientes para calcular el impuesto</p>
            <p className="text-sm text-slate-400 mt-2">Agrega ingresos y gastos para ver tu cálculo tributario</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

// Sección de Sugerencias
const SugerenciasSection = ({ sugerencias }) => {
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 1: return 'border-rose-500 bg-gradient-to-br from-rose-50 to-red-50';
      case 2: return 'border-amber-500 bg-gradient-to-br from-amber-50 to-yellow-50';
      case 3: return 'border-emerald-500 bg-gradient-to-br from-emerald-50 to-green-50';
      default: return 'border-slate-500 bg-gradient-to-br from-slate-50 to-gray-50';
    }
  };

  const getPriorityText = (priority) => {
    switch (priority) {
      case 1: return 'Alta Prioridad';
      case 2: return 'Media Prioridad';
      case 3: return 'Baja Prioridad';
      default: return 'Prioridad';
    }
  };

  return (
    <Card className="shadow-lg border-sky-100">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-sky-800">
          <Lightbulb className="w-5 h-5" />
          Sugerencias de Financiamiento
        </CardTitle>
        <CardDescription>
          Recomendaciones personalizadas basadas en tu situación financiera actual
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {sugerencias.map((sugerencia, index) => (
            <Card key={index} className={`${getPriorityColor(sugerencia.prioridad)} border-2 hover:shadow-lg transition-shadow`}>
              <CardContent className="p-6">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-lg">{sugerencia.tipo}</h3>
                    <Badge variant="outline" className="mt-1">
                      {getPriorityText(sugerencia.prioridad)}
                    </Badge>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-slate-600">Monto Sugerido</p>
                    <p className="text-xl font-bold">S/ {sugerencia.monto_sugerido.toFixed(2)}</p>
                  </div>
                </div>
                
                <p className="text-slate-700 mb-3">{sugerencia.descripcion}</p>
                
                <div className="bg-white/70 p-3 rounded-lg border">
                  <p className="text-sm font-medium text-slate-600 mb-1">Beneficio:</p>
                  <p className="text-sm">{sugerencia.beneficio}</p>
                </div>
              </CardContent>
            </Card>
          ))}
          {sugerencias.length === 0 && (
            <p className="text-center text-slate-500 py-8">No hay sugerencias disponibles</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

// Sección de Reportes
const ReportesSection = () => {
  const [reportes, setReportes] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchReportes();
  }, []);

  const fetchReportes = async () => {
    try {
      const response = await axios.get(`${API}/reportes-sunat`);
      setReportes(response.data);
    } catch (error) {
      console.error('Error fetching reportes:', error);
    }
  };

  const generateReport = async (tipo, periodo) => {
    setLoading(true);
    try {
      await axios.post(`${API}/reporte-sunat`, null, {
        params: { tipo_reporte: tipo, periodo }
      });
      toast.success('Reporte generado exitosamente');
      fetchReportes();
    } catch (error) {
      toast.error('Error al generar reporte');
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async (reporteId, nombreArchivo) => {
    try {
      const response = await axios.get(`${API}/reportes-sunat/${reporteId}/download`, {
        responseType: 'blob'
      });
      
      // Crear un enlace de descarga
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', nombreArchivo);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Reporte descargado exitosamente');
    } catch (error) {
      toast.error('Error al descargar reporte');
    }
  };

  return (
    <Card className="shadow-lg border-sky-100">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-sky-800">
          <FileText className="w-5 h-5" />
          Reportes SUNAT
        </CardTitle>
        <CardDescription>
          Genera y descarga reportes financieros para declaraciones tributarias
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Button 
            onClick={() => generateReport('ingresos', '2024')} 
            disabled={loading}
            className="h-16 flex-col gap-2 bg-gradient-to-r from-emerald-500 to-green-500 hover:from-emerald-600 hover:to-green-600"
          >
            <FileText className="w-6 h-6" />
            Reporte de Ingresos 2024
          </Button>
          <Button 
            onClick={() => generateReport('gastos', '2024')} 
            disabled={loading}
            className="h-16 flex-col gap-2 bg-gradient-to-r from-rose-500 to-red-500 hover:from-rose-600 hover:to-red-600"
          >
            <BarChart3 className="w-6 h-6" />
            Reporte de Gastos 2024
          </Button>
          <Button 
            onClick={() => generateReport('completo', '2024')} 
            disabled={loading}
            className="h-16 flex-col gap-2 bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600"
          >
            <PieChart className="w-6 h-6" />
            Reporte Completo 2024
          </Button>
        </div>

        <Separator />

        <div className="space-y-3">
          <h3 className="font-semibold">Reportes Generados</h3>
          {reportes.map(reporte => (
            <Card key={reporte.id} className="bg-gradient-to-r from-sky-50 to-cyan-50 border-sky-200">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">{reporte.tipo_reporte} - {reporte.periodo}</p>
                    <p className="text-sm text-slate-600">
                      Generado: {new Date(reporte.created_at).toLocaleDateString('es-PE')}
                    </p>
                    <p className="text-xs text-slate-500">Archivo: {reporte.nombre_archivo}</p>
                  </div>
                  <Button 
                    size="sm" 
                    onClick={() => downloadReport(reporte.id, reporte.nombre_archivo)}
                    className="bg-sky-600 hover:bg-sky-700"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Descargar CSV
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
          {reportes.length === 0 && (
            <p className="text-center text-slate-500 py-4">No hay reportes generados</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

// Sección de Administrador
const AdminSection = () => {
  const [users, setUsers] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchUsers();
    fetchStats();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/admin/users`);
      setUsers(response.data);
    } catch (error) {
      toast.error('Error al cargar usuarios');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API}/admin/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <div className="space-y-6">
      <Card className="shadow-lg border-amber-200">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-amber-800">
            <Shield className="w-5 h-5" />
            Panel de Administración
          </CardTitle>
          <CardDescription>
            Vista completa de usuarios y estadísticas del sistema
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Estadísticas */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatsCard
            title="Total Usuarios"
            value={stats.total_usuarios}
            icon={<Users className="w-6 h-6 text-sky-600" />}
            bgColor="bg-gradient-to-br from-sky-50 to-blue-100"
          />
          <StatsCard
            title="Total Ingresos"
            value={stats.total_ingresos}
            icon={<TrendingUp className="w-6 h-6 text-emerald-600" />}
            bgColor="bg-gradient-to-br from-emerald-50 to-green-100"
          />
          <StatsCard
            title="Total Gastos"
            value={stats.total_gastos}
            icon={<TrendingDown className="w-6 h-6 text-rose-600" />}
            bgColor="bg-gradient-to-br from-rose-50 to-red-100"
          />
          <StatsCard
            title="Simulaciones"
            value={stats.total_simulaciones}
            icon={<Calculator className="w-6 h-6 text-violet-600" />}
            bgColor="bg-gradient-to-br from-violet-50 to-purple-100"
          />
        </div>
      )}

      {/* Lista de usuarios */}
      <Card className="shadow-lg border-sky-100">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-sky-800">
            <Users className="w-5 h-5" />
            Usuarios Registrados
          </CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <p className="text-center py-8">Cargando usuarios...</p>
          ) : (
            <div className="space-y-3">
              {users.map(user => (
                <Card key={user.id} className="bg-gradient-to-r from-sky-50 to-cyan-50 border-sky-200">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <p className="font-medium">{user.nombre} {user.apellido}</p>
                          {user.is_admin && (
                            <Badge className="bg-amber-100 text-amber-800">
                              <Shield className="w-3 h-3 mr-1" />
                              Admin
                            </Badge>
                          )}
                        </div>
                        <p className="text-sm text-slate-600">{user.email}</p>
                        <p className="text-xs text-slate-500">DNI: {user.dni} | Ocupación: {user.ocupacion}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-slate-600">Registrado</p>
                        <p className="text-xs text-slate-500">
                          {new Date(user.created_at).toLocaleDateString('es-PE')}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
              {users.length === 0 && (
                <p className="text-center text-slate-500 py-8">No hay usuarios registrados</p>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppContent />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

const AppContent = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-sky-50 to-cyan-100 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-br from-sky-400 to-cyan-500 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
            <DollarSign className="w-8 h-8 text-white" />
          </div>
          <p className="text-slate-600">Cargando...</p>
        </div>
      </div>
    );
  }

  return user ? <Dashboard /> : <LoginForm />;
};

export default App;