// session.js - Manejo de sesion compartido entre todas las paginas
// Ajusta esta URL si el backend corre en otra direccion/puerto
const API_BASE_URL = 'http://127.0.0.1:8000';

function guardarSesion(data) {
    sessionStorage.setItem('petshop_session', JSON.stringify({
        esAdmin: !!data.es_admin,
        idCliente: data.id_cliente ?? null,
        nombre: data.nombre ?? null,
        correo: data.correo ?? null,
    }));
}

function obtenerSesion() {
    const raw = sessionStorage.getItem('petshop_session');
    if (!raw) return null;
    try {
        return JSON.parse(raw);
    } catch (e) {
        return null;
    }
}

function cerrarSesion() {
    sessionStorage.removeItem('petshop_session');
}

// Redirige al login si no hay un cliente autenticado (paginas de cliente)
function requerirSesionCliente() {
    const sesion = obtenerSesion();
    if (!sesion || sesion.esAdmin || !sesion.idCliente) {
        window.location.href = 'login.html';
        return null;
    }
    return sesion;
}

// Redirige al login si no hay un administrador autenticado (panel admin)
function requerirSesionAdmin() {
    const sesion = obtenerSesion();
    if (!sesion || !sesion.esAdmin) {
        window.location.href = 'login.html';
        return null;
    }
    return sesion;
}
