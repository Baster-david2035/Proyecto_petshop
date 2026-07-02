let sesionActual = null;
let mascotasCache = {};
const POLL_INTERVAL_MS = 5000;

const ESTADO_INFO = {
    'En revision': { clase: 'status-pending', texto: 'En revisión', emoji: '⏳' },
    'Aprobada': { clase: 'status-approved', texto: 'Aprobada', emoji: '🎉' },
    'Rechazada': { clase: 'status-rejected', texto: 'Rechazada', emoji: '😔' },
    'Finalizada': { clase: 'status-finalized', texto: 'Finalizada', emoji: '✅' },
};

document.addEventListener('DOMContentLoaded', () => {
    sesionActual = requerirSesionCliente();
    if (!sesionActual) return;

    setupCarousel();
    cargarMisSolicitudes();
    setInterval(cargarMisSolicitudes, POLL_INTERVAL_MS);
});

function setupCarousel() {
    const track = document.getElementById('carouselTrack');
    const btnPrev = document.getElementById('btnPrev');
    const btnNext = document.getElementById('btnNext');

    let currentIndex = 0;
    const totalCards = 4;

    function moveCarousel() {
        track.style.transform = `translateX(-${currentIndex * 25}%)`;
    }

    btnNext.addEventListener('click', () => {
        currentIndex = (currentIndex < totalCards - 1) ? currentIndex + 1 : 0;
        moveCarousel();
    });

    btnPrev.addEventListener('click', () => {
        currentIndex = (currentIndex > 0) ? currentIndex - 1 : totalCards - 1;
        moveCarousel();
    });
}

async function obtenerNombreMascota(idMascota) {
    if (mascotasCache[idMascota]) return mascotasCache[idMascota];
    try {
        const res = await fetch(`${API_BASE_URL}/mascotas/${idMascota}`);
        if (!res.ok) return 'Mascota';
        const mascota = await res.json();
        mascotasCache[idMascota] = mascota.nombre;
        return mascota.nombre;
    } catch (e) {
        return 'Mascota';
    }
}

async function cargarMisSolicitudes() {
    const container = document.getElementById('user-requests-container');

    try {
        const res = await fetch(`${API_BASE_URL}/solicitudes/cliente/${sesionActual.idCliente}`);
        if (!res.ok) throw new Error('No se pudieron cargar las solicitudes');

        const solicitudes = await res.json();

        if (solicitudes.length === 0) {
            container.innerHTML = `<p class="receipt-empty-text" id="no-requests-message">Aún no tienes solicitudes de adopción. <a href="adopcion.html">¡Encuentra a tu compañero ideal!</a></p>`;
            return;
        }

        const tarjetas = await Promise.all(solicitudes.map(renderSolicitudCard));
        container.innerHTML = tarjetas.join('');

    } catch (error) {
        console.error('Error cargando solicitudes:', error);
        container.innerHTML = `<p class="receipt-empty-text">No pudimos cargar tus solicitudes en este momento.</p>`;
    }
}

async function renderSolicitudCard(solicitud) {
    const nombreMascota = await obtenerNombreMascota(solicitud.id_mascota);
    const info = ESTADO_INFO[solicitud.estado] || { clase: 'status-pending', texto: solicitud.estado, emoji: 'ℹ️' };

    let mensaje = '';
    let clickHandler = '';

    if (solicitud.estado === 'En revision') {
        mensaje = 'Tu solicitud está siendo revisada por nuestro equipo. Te avisaremos apenas haya una respuesta.';
    } else if (solicitud.estado === 'Aprobada') {
        mensaje = `🎉 ¡Felicidades! Tu solicitud fue aprobada. <strong class="action-highlight">Toca esta tarjeta para contratar sus primeros servicios</strong> y agendar tu fecha de retiro en el local.`;
        clickHandler = `onclick="window.location.href='servicios.html?solicitud=${solicitud.id_solicitud}'" style="cursor:pointer;"`;
    } else if (solicitud.estado === 'Rechazada') {
        mensaje = 'Lamentablemente tu solicitud no fue aprobada en esta ocasión. Puedes intentar con otra mascota.';
    } else if (solicitud.estado === 'Finalizada') {
        mensaje = 'Esta adopción ya fue pagada y finalizada. ¡Gracias por darle un hogar! No es posible volver a pagar por esta solicitud.';
    }

    return `
        <div class="user-request-item" id="solicitud-${solicitud.id_solicitud}" ${clickHandler}>
            <div class="request-flex-left">
                <div class="pet-avatar-mini">🐶</div>
                <div class="request-info-block">
                    <h4>Solicitud de adopción para <strong class="pet-highlight">${nombreMascota}</strong></h4>
                    <p class="request-feedback">${info.emoji} ${mensaje}</p>
                </div>
            </div>
            <span class="badge-status ${info.clase}">${info.texto}</span>
        </div>
    `;
}
