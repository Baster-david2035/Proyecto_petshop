let mascotasMap = {};
let clientesMap = {};

// --- 1. CARGA INICIAL DE DATOS DESDE LA API ---
document.addEventListener('DOMContentLoaded', () => {
    const sesion = requerirSesionAdmin();
    if (!sesion) return;

    fetchDashboardData();
    setupSearchFilters();
    setupFormListeners();
});

async function fetchDashboardData() {
    try {
        const [clients, requests, pets, services, adoptions] = await Promise.all([
            fetch(`${API_BASE_URL}/clientes/`).then(res => res.json()),
            fetch(`${API_BASE_URL}/solicitudes/`).then(res => res.json()),
            fetch(`${API_BASE_URL}/mascotas/`).then(res => res.json()),
            fetch(`${API_BASE_URL}/servicios/`).then(res => res.json()),
            fetch(`${API_BASE_URL}/adopciones/`).then(res => res.json()),
        ]);

        mascotasMap = Object.fromEntries(pets.map(p => [p.id_mascota, p]));
        clientesMap = Object.fromEntries(clients.map(c => [c.id_cliente, c]));

        renderClients(clients);
        renderRequests(requests);
        renderPets(pets);
        renderServices(services);
        renderAdoptions(adoptions);
        renderFinance(adoptions);
        updateDashboardKPIs(clients, requests, pets, services, adoptions);

    } catch (error) {
        console.error('Error cargando los datos del servidor:', error);
    }
}

// --- 2. RENDERIZADORES DE PLANTILLAS DINÁMICAS ---
function renderClients(clients) {
    const container = document.getElementById('table-clients-body');
    container.innerHTML = clients.map(client => `
        <tr class="client-row">
            <td>#${client.id_cliente}</td>
            <td class="client-name">${client.nombre}</td>
            <td class="client-email">${client.correo}</td>
            <td><span class="status active-status">${client.estado}</span></td>
        </tr>
    `).join('');
}

function renderRequests(requests) {
    const container = document.getElementById('requests-list');
    const pendientes = requests.filter(r => r.estado === 'En revision');

    if (pendientes.length === 0) {
        container.innerHTML = `<p class="receipt-empty-text">No hay solicitudes pendientes por revisar.</p>`;
        return;
    }

    container.innerHTML = pendientes.map(req => {
        const mascota = mascotasMap[req.id_mascota];
        const cliente = clientesMap[req.id_cliente];
        return `
        <div class="request-card" data-id="${req.id_solicitud}">
            <div class="request-header" style="display: flex; justify-content: space-between; align-items: center;">
                <span class="pet-target-badge">Para: <strong class="req-pet">${mascota ? mascota.nombre : '—'}</strong></span>
                <span class="status-pending" style="background: #fff3cd; color: #856404; padding: 2px 6px; border-radius: 4px; font-size: 12px;">${req.estado}</span>
            </div>
            <div class="request-body" style="margin: 8px 0;">
                <p><strong>Postulante:</strong> <span class="req-user">${cliente ? cliente.nombre : '—'}</span></p>
                <p>"${req.motivo}"</p>
            </div>
            <div class="request-actions" style="display: flex; gap: 5px;">
                <button class="btn-approve" onclick="handleRequestAction(${req.id_solicitud}, 'approve')">Aprobar</button>
                <button class="btn-reject" onclick="handleRequestAction(${req.id_solicitud}, 'reject')">Rechazar</button>
            </div>
        </div>
    `;
    }).join('');
}

function renderPets(pets) {
    const container = document.getElementById('all-pets-list');
    container.innerHTML = pets.map(pet => {
        let emoji = "🐶";
        const razaLower = pet.raza.toLowerCase();
        if (razaLower.includes('gato')) {
            emoji = "🐱";
        } else if (razaLower.includes('conejo')) {
            emoji = "🐰";
        } else if (razaLower.includes('loro')) {
            emoji = "🦜";
        } else if (razaLower.includes('ave') || razaLower.includes('pajaro') || razaLower.includes('periquito')) {
            emoji = "🐦";
        } else if (razaLower.includes('hamster') || razaLower.includes('cuyo') || razaLower.includes('cobaya') || razaLower.includes('raton')) {
            emoji = "🐹";
        } else if (razaLower.includes('huron')) {
            emoji = "🦦";
        } else if (razaLower.includes('pez') || razaLower.includes('pescado') || razaLower.includes('acuatico')) {
            emoji = "🐟";
        } else if (razaLower.includes('tortuga') || razaLower.includes('iguana') || razaLower.includes('lagarto') || razaLower.includes('reptil')) {
            emoji = "🦎";
        } else if (razaLower.includes('cerdo') || razaLower.includes('mini pig') || razaLower.includes('puerquito')) {
            emoji = "🐷";
        } else if (!razaLower.includes('perro')) {
            emoji = "🐾"; 
        }
        return `
            <div class="preview-item pet-item-row" data-id="${pet.id_mascota}" style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; gap: 15px; align-items: center;">
                    <div style="font-size: 24px;">${emoji}</div>
                    <div>
                        <h4 class="pet-title-name" style="margin:0;">${pet.nombre}</h4>
                        <p style="margin: 2px 0 0 0; font-size: 13px; color: #666;">Raza: ${pet.raza} | Edad: ${pet.edad} años | Estado: ${pet.estado}</p>
                    </div>
                </div>
                <div style="display: flex; gap: 5px;">
                    <button class="btn-manage-delete" onclick="deletePet(${pet.id_mascota})">🗑️</button>
                </div>
            </div>
        `;
    }).join('');
}

function renderServices(services) {
    const container = document.getElementById('services-list');
    container.innerHTML = services.map(srv => `
        <div class="preview-item service-item-row" data-id="${srv.id_servicio}" style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; gap: 15px; align-items: center;">
                <div class="item-avatar" style="background: #e0f2fe; color: #0369a1; padding: 8px; border-radius:50%; font-size:18px;">🩺</div>
                <div class="item-details">
                    <h4 class="service-title-name" style="margin:0;">${srv.nombre}</h4>
                    <p style="margin:0; font-size:13px; color:#666;">${srv.tipo_servicio}</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div class="item-price" style="font-weight:bold;">₡${parseFloat(srv.costo).toFixed(2)}</div>
                <div style="display: flex; gap: 5px;">
                    <button class="btn-manage-delete" onclick="deleteService(${srv.id_servicio})">🗑️</button>
                </div>
            </div>
        </div>
    `).join('');
}

// Registro: historial de todas las adopciones ya concretadas (pagadas)
function renderAdoptions(adoptions) {
    const container = document.getElementById('table-adoptions-body');

    if (adoptions.length === 0) {
        container.innerHTML = `<tr><td colspan="5" style="text-align:center;color:#94a3b8;">Aún no se ha registrado ninguna adopción.</td></tr>`;
        return;
    }

    const ordenadas = [...adoptions].sort((a, b) => b.id_adopcion - a.id_adopcion);

    container.innerHTML = ordenadas.map(ad => {
        const mascota = mascotasMap[ad.id_mascota];
        const cliente = clientesMap[ad.id_cliente];
        return `
            <tr class="adoption-row" data-id="${ad.id_adopcion}">
                <td>#${ad.id_adopcion}</td>
                <td class="adoption-client">${cliente ? cliente.nombre : `Cliente #${ad.id_cliente}`}</td>
                <td class="adoption-pet">${mascota ? mascota.nombre : `Mascota #${ad.id_mascota}`}</td>
                <td>${formatearFecha(ad.fecha_adopcion)}</td>
                <td>₡${parseFloat(ad.costo).toFixed(2)}</td>
            </tr>
        `;
    }).join('');
}

// Finanzas: recaudación total, cantidad de adopciones cobradas y ticket promedio
function renderFinance(adoptions) {
    const total = adoptions.reduce((sum, ad) => sum + parseFloat(ad.costo), 0);
    const cantidad = adoptions.length;
    const promedio = cantidad > 0 ? total / cantidad : 0;

    document.getElementById('finance-total').innerText = `₡${total.toFixed(2)}`;
    document.getElementById('finance-count').innerText = cantidad;
    document.getElementById('finance-average').innerText = `₡${promedio.toFixed(2)}`;

    const container = document.getElementById('table-finance-body');

    if (adoptions.length === 0) {
        container.innerHTML = `<tr><td colspan="5" style="text-align:center;color:#94a3b8;">Todavía no hay ingresos registrados.</td></tr>`;
        return;
    }

    const ordenadas = [...adoptions].sort((a, b) => b.id_adopcion - a.id_adopcion);

    container.innerHTML = ordenadas.map(ad => {
        const mascota = mascotasMap[ad.id_mascota];
        const cliente = clientesMap[ad.id_cliente];
        return `
            <tr>
                <td>#${ad.id_adopcion}</td>
                <td>${cliente ? cliente.nombre : `Cliente #${ad.id_cliente}`}</td>
                <td>${mascota ? mascota.nombre : `Mascota #${ad.id_mascota}`}</td>
                <td>${formatearFecha(ad.fecha_adopcion)}</td>
                <td style="color:#22c55e;font-weight:bold;">₡${parseFloat(ad.costo).toFixed(2)}</td>
            </tr>
        `;
    }).join('');
}

function formatearFecha(fechaStr) {
    try {
        const fecha = new Date(fechaStr);
        if (isNaN(fecha.getTime())) return fechaStr;
        return fecha.toLocaleDateString('es-ES', { year: 'numeric', month: '2-digit', day: '2-digit' });
    } catch (e) {
        return fechaStr;
    }
}

// --- 3. ACCIONES HACIA LA API (POST / DELETE / PATCH) ---
function setupFormListeners() {
    // Agregar Cliente
    document.getElementById('form-add-client').addEventListener('submit', async function (e) {
        e.preventDefault();
        const payload = {
            nombre: document.getElementById('client-name-input').value,
            telefono: document.getElementById('client-phone-input').value,
            correo: document.getElementById('client-email-input').value,
        };

        try {
            const res = await fetch(`${API_BASE_URL}/clientes/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            const data = await res.json();
            if (res.ok) {
                this.reset();
                fetchDashboardData();
            } else {
                alert(data.detail || 'No se pudo agregar el cliente.');
            }
        } catch (err) { console.error("Error al guardar cliente:", err); }
    });

    // Agregar Mascota
    document.getElementById('form-add-pet').addEventListener('submit', async function (e) {
        e.preventDefault();
        const payload = {
            nombre: document.getElementById('pet-name-input').value,
            raza: document.getElementById('pet-breed-input').value,
            edad: parseInt(document.getElementById('pet-age-input').value, 10),
            estado: 'Disponible',
        };

        try {
            const res = await fetch(`${API_BASE_URL}/mascotas/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            if (res.ok) {
                this.reset();
                fetchDashboardData();
            }
        } catch (err) { console.error("Error al guardar mascota:", err); }
    });

    // Agregar Servicio
    document.getElementById('form-add-service').addEventListener('submit', async function (e) {
        e.preventDefault();
        const payload = {
            nombre: document.getElementById('service-name-input').value,
            costo: parseFloat(document.getElementById('service-price-input').value),
            tipo_servicio: document.getElementById('service-desc-input').value,
        };

        try {
            const res = await fetch(`${API_BASE_URL}/servicios/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            if (res.ok) {
                this.reset();
                fetchDashboardData();
            }
        } catch (err) { console.error("Error al guardar servicio:", err); }
    });
}

// Resolver solicitudes de adopción (Aprobar/Rechazar)
async function handleRequestAction(id, action) {
    const nuevoEstado = action === 'approve' ? 'Aprobada' : 'Rechazada';
    try {
        const res = await fetch(`${API_BASE_URL}/solicitudes/${id}/estado?estado=${encodeURIComponent(nuevoEstado)}`, {
            method: 'PATCH',
        });
        if (res.ok) fetchDashboardData();
    } catch (err) { console.error(err); }
}

// Eliminar Mascota
async function deletePet(id) {
    if (!confirm("¿Seguro que deseas dar de baja esta mascota?")) return;
    try {
        const res = await fetch(`${API_BASE_URL}/mascotas/${id}`, { method: 'DELETE' });
        if (res.ok) fetchDashboardData();
    } catch (err) { console.error(err); }
}

// Eliminar Servicio
async function deleteService(id) {
    if (!confirm("¿Deseas eliminar este servicio de manera definitiva?")) return;
    try {
        const res = await fetch(`${API_BASE_URL}/servicios/${id}`, { method: 'DELETE' });
        if (res.ok) fetchDashboardData();
    } catch (err) { console.error(err); }
}

// --- 4. SISTEMAS AUXILIARES (KPIs Y FILTRADO LOCAL) ---
function updateDashboardKPIs(clients, requests, pets, services, adoptions) {
    document.getElementById('kpi-users').innerText = clients.length;
    document.getElementById('kpi-requests').innerText = requests.filter(r => r.estado === 'En revision').length;
    document.getElementById('kpi-pets').innerText = pets.length;
    document.getElementById('kpi-services').innerText = services.length;

    const totalRecaudado = adoptions.reduce((sum, ad) => sum + parseFloat(ad.costo), 0);
    document.getElementById('kpi-revenue').innerText = `₡${totalRecaudado.toFixed(2)}`;
}

function setupSearchFilters() {
    document.getElementById('search-clients').addEventListener('keyup', function () {
        const query = this.value.toLowerCase();
        document.querySelectorAll('.client-row').forEach(row => {
            const name = row.querySelector('.client-name').innerText.toLowerCase();
            const email = row.querySelector('.client-email').innerText.toLowerCase();
            row.style.display = (name.includes(query) || email.includes(query)) ? "" : "none";
        });
    });

    document.getElementById('search-requests').addEventListener('keyup', function () {
        const query = this.value.toLowerCase();
        document.querySelectorAll('.request-card').forEach(card => {
            const pet = card.querySelector('.req-pet').innerText.toLowerCase();
            const user = card.querySelector('.req-user').innerText.toLowerCase();
            card.style.display = (pet.includes(query) || user.includes(query)) ? "" : "none";
        });
        document.querySelectorAll('.pet-item-row').forEach(row => {
            const petName = row.querySelector('.pet-title-name').innerText.toLowerCase();
            row.style.display = petName.includes(query) ? "" : "none";
        });
    });

    document.getElementById('search-services').addEventListener('keyup', function () {
        const query = this.value.toLowerCase();
        document.querySelectorAll('.service-item-row').forEach(item => {
            const srvName = item.querySelector('.service-title-name').innerText.toLowerCase();
            item.style.display = srvName.includes(query) ? "" : "none";
        });
    });

    const searchAdoptions = document.getElementById('search-adoptions');
    if (searchAdoptions) {
        searchAdoptions.addEventListener('keyup', function () {
            const query = this.value.toLowerCase();
            document.querySelectorAll('.adoption-row').forEach(row => {
                const cliente = row.querySelector('.adoption-client').innerText.toLowerCase();
                const mascota = row.querySelector('.adoption-pet').innerText.toLowerCase();
                row.style.display = (cliente.includes(query) || mascota.includes(query)) ? "" : "none";
            });
        });
    }
}
