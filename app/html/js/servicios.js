let sesionActual = null;
let solicitudActual = null;

// Elementos Globales del DOM
const servicesContainer = document.getElementById('services-list-container');
const receiptDiv = document.getElementById('checkout-receipt');
const totalSpan = document.getElementById('checkout-total');
const proceedBtn = document.getElementById('btn-proceed-pay');
const pickupDateInput = document.getElementById('pickup-date');

const modalOverlay = document.getElementById('paymentModal');
const modalPayStep = document.getElementById('modal-pay-step');
const modalInvoiceStep = document.getElementById('modal-invoice-step');
const modalPaymentTotal = document.getElementById('modal-payment-total');

// Bloquear fechas pasadas en el calendario
const today = new Date().toISOString().split('T')[0];
pickupDateInput.setAttribute('min', today);

document.addEventListener('DOMContentLoaded', async () => {
    sesionActual = requerirSesionCliente();
    if (!sesionActual) return;

    const params = new URLSearchParams(window.location.search);
    const idSolicitud = params.get('solicitud');

    if (!idSolicitud) {
        alert('Debes acceder a esta página desde una solicitud aprobada en "Mis solicitudes".');
        window.location.href = 'home.html';
        return;
    }

    const valido = await cargarSolicitud(idSolicitud);
    if (!valido) return;

    fetchActiveServices();
    setupInterfaceEvents();
});

// --- VALIDAR LA SOLICITUD ANTES DE PERMITIR EL PAGO ---
async function cargarSolicitud(idSolicitud) {
    try {
        const res = await fetch(`${API_BASE_URL}/solicitudes/${idSolicitud}`);
        if (!res.ok) throw new Error('Solicitud no encontrada');
        const solicitud = await res.json();

        if (solicitud.id_cliente !== sesionActual.idCliente) {
            alert('Esta solicitud no pertenece a tu cuenta.');
            window.location.href = 'home.html';
            return false;
        }

        if (solicitud.estado === 'Finalizada') {
            alert('Esta solicitud ya fue atendida y pagada. No puedes volver a pagar por ella.');
            window.location.href = 'home.html';
            return false;
        }

        if (solicitud.estado !== 'Aprobada') {
            alert('Tu solicitud todavía no ha sido aprobada por el administrador.');
            window.location.href = 'home.html';
            return false;
        }

        solicitudActual = solicitud;
        return true;
    } catch (error) {
        console.error(error);
        alert('No se pudo validar la solicitud.');
        window.location.href = 'home.html';
        return false;
    }
}

// --- 1. SOLICITAR SERVICIOS A LA API (GET) ---
async function fetchActiveServices() {
    try {
        const response = await fetch(`${API_BASE_URL}/servicios/`);
        if (!response.ok) throw new Error('Fallo al obtener servicios');

        const services = await response.json();
        renderServicesList(services);
    } catch (error) {
        console.error('Error del catálogo:', error);
        servicesContainer.innerHTML = `<p class="receipt-empty-text">No pudimos conectar con los servicios. Reintenta pronto.</p>`;
    }
}

// --- 2. RENDERIZACIÓN DINÁMICA ---
function renderServicesList(services) {
    if (services.length === 0) {
        servicesContainer.innerHTML = `<p class="receipt-empty-text">No hay servicios disponibles listados para contratación.</p>`;
        return;
    }

    servicesContainer.innerHTML = services.map(service => `
        <label class="service-selection-card" id="card-${service.id_servicio}">
            <input type="checkbox" class="service-checkbox" value="${service.costo}" data-id="${service.id_servicio}" data-name="${service.nombre}">
            <div class="service-select-info">
                <h4>${service.nombre}</h4>
                <p>${service.tipo_servicio}</p>
            </div>
            <span class="service-select-price">₡${parseFloat(service.costo).toFixed(2)}</span>
        </label>
    `).join('');

    document.querySelectorAll('.service-checkbox').forEach(box => {
        box.addEventListener('change', calculateSummary);
    });
}

// --- 3. CÁLCULO DE RESUMEN REACTIVO---
function calculateSummary() {
    let total = 0;
    let receiptHTML = '';
    const checkboxes = document.querySelectorAll('.service-checkbox');

    checkboxes.forEach(box => {
        const card = document.getElementById(`card-${box.getAttribute('data-id')}`);

        if (box.checked) {
            total += parseFloat(box.value);
            if (card) card.classList.add('card-selected');

            receiptHTML += `
                <div class="receipt-item-row">
                    <span>• ${box.getAttribute('data-name')}</span>
                    <strong>₡${parseFloat(box.value).toFixed(2)}</strong>
                </div>`;
        } else {
            if (card) card.classList.remove('card-selected');
        }
    });

    if (total > 0) {
        receiptDiv.innerHTML = receiptHTML;
        totalSpan.innerText = `₡${total.toFixed(2)}`;
    } else {
        receiptDiv.innerHTML = `<p class="receipt-empty-text">No has seleccionado ningún servicio aún.</p>`;
        totalSpan.innerText = '₡0.00';
    }

    validateFormState();
}

function validateFormState() {
    const checkboxes = document.querySelectorAll('.service-checkbox');
    const hasServices = Array.from(checkboxes).some(box => box.checked);
    const hasDate = pickupDateInput.value !== "";

    if (hasServices && hasDate) {
        proceedBtn.removeAttribute('disabled');
        proceedBtn.classList.remove('btn-disabled');
    } else {
        proceedBtn.setAttribute('disabled', 'true');
        proceedBtn.classList.add('btn-disabled');
    }
}

// --- 4. CONTROL DE PASARELA ---
function setupInterfaceEvents() {
    pickupDateInput.addEventListener('change', validateFormState);

    proceedBtn.addEventListener('click', () => {
        modalPaymentTotal.innerText = totalSpan.innerText;
        modalPayStep.style.display = 'block';
        modalInvoiceStep.style.display = 'none';
        modalOverlay.classList.add('show-modal');
        modalPayStep.style.transform = 'translateY(0)';
    });

    document.getElementById('btn-close-payment').addEventListener('click', () => {
        modalOverlay.classList.remove('show-modal');
        modalPayStep.style.transform = 'translateY(-20px)';
    });

    document.getElementById('paymentForm').addEventListener('submit', handlePaymentSubmit);

    document.getElementById('btn-invoice-done').addEventListener('click', () => {
        window.location.href = 'home.html';
    });
}

// --- 5. REGISTRO DEL PAGO EN LA API ---
async function handlePaymentSubmit(e) {
    e.preventDefault();

    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;

    const total = parseFloat(totalSpan.innerText.replace('₡', ''));

    const paymentPayload = {
        id_cliente: sesionActual.idCliente,
        id_mascota: solicitudActual.id_mascota,
        id_solicitud: solicitudActual.id_solicitud,
        costo: total,
    };

    try {
        const response = await fetch(`${API_BASE_URL}/adopciones/pagar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(paymentPayload),
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || 'No se pudo procesar el pago.');
            submitBtn.disabled = false;
            return;
        }

        renderFinalInvoice(data.id_adopcion);

    } catch (error) {
        console.error('Error procesando pago:', error);
        alert('Error de conexión con el servidor. Inténtalo nuevamente.');
        submitBtn.disabled = false;
    }
}

// Pintar la interfaz tipo Ticket de Caja Registradora
function renderFinalInvoice(orderNumber) {
    const checkboxes = document.querySelectorAll('.service-checkbox');
    const todayFormatted = new Date().toLocaleDateString('es-ES', { year: 'numeric', month: '2-digit', day: '2-digit' });
    const selectedDate = new Date(pickupDateInput.value + 'T00:00:00');
    const pickupFormatted = selectedDate.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    document.getElementById('invoice-order-number').innerText = `Orden: #PS-${orderNumber}`;
    document.getElementById('inv-current-date').innerText = todayFormatted;
    document.getElementById('inv-pickup-date').innerText = pickupFormatted;
    document.getElementById('inv-total').innerText = totalSpan.innerText;

    let itemsHTML = '';
    checkboxes.forEach(box => {
        if (box.checked) {
            itemsHTML += `
                <div class="invoice-breakdown-row">
                    <span>${box.getAttribute('data-name')}</span>
                    <span>$${parseFloat(box.value).toFixed(2)}</span>
                </div>`;
        }
    });
    document.getElementById('inv-items-list').innerHTML = itemsHTML;

    modalPayStep.style.display = 'none';
    modalInvoiceStep.style.display = 'flex';
}
