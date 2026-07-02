let sesionActual = null;

// --- 1. CARGA INICIAL ---
document.addEventListener('DOMContentLoaded', () => {
    sesionActual = requerirSesionCliente();
    if (!sesionActual) return;

    fetchAvailablePets();
    setupModalListeners();
    setupFormSubmit();
});

// Obtener solo las mascotas disponibles para adopcion desde el servidor
async function fetchAvailablePets() {
    try {
        const response = await fetch(`${API_BASE_URL}/mascotas/disponibles`);
        if (!response.ok) throw new Error('Error al conectar con la API');

        const pets = await response.json();
        renderPetGallery(pets);
    } catch (error) {
        console.error('No se pudieron cargar las mascotas:', error);
        document.getElementById('pets-gallery-container').innerHTML = `
            <p style="grid-column: 1/-1; text-align:center; color: #64748b;">
                Por el momento no logramos conectar con el sistema. Inténtalo más tarde.
            </p>
        `;
    }
}

// --- 2. RENDERIZADO DINÁMICO DE LA LISTA ---
function renderPetGallery(pets) {
    const container = document.getElementById('pets-gallery-container');

    if (pets.length === 0) {
        container.innerHTML = '<p style="text-align:center;">No hay mascotas disponibles para adopción actualmente.</p>';
        return;
    }

    container.innerHTML = pets.map(pet => {
        let badgeClass = 'badge-generico';
        let icon = '🐾';
        const breedLower = (pet.raza || '').toLowerCase();

        if (breedLower.includes('perro')) { 
            badgeClass = 'badge-perro'; 
            icon = '🐶'; 
        } else if (breedLower.includes('gato')) { 
            badgeClass = 'badge-gato'; 
            icon = '🐱'; 
        } else if (breedLower.includes('loro')) { 
            badgeClass = 'badge-loro'; 
            icon = '🦜'; 
        } else if (breedLower.includes('ave') || breedLower.includes('pajaro') || breedLower.includes('periquito')) { 
            badgeClass = 'badge-ave'; 
            icon = '🐦'; 
        } else if (breedLower.includes('conejo')) { 
            badgeClass = 'badge-conejo'; 
            icon = '🐰'; 
        } else if (breedLower.includes('hamster') || breedLower.includes('cuyo') || breedLower.includes('cobaya') || breedLower.includes('raton')) { 
            badgeClass = 'badge-roedor'; 
            icon = '🐹'; 
        } else if (breedLower.includes('huron')) { 
            badgeClass = 'badge-huron'; 
            icon = '🦦';
        } else if (breedLower.includes('pez') || breedLower.includes('pescado')) { 
            badgeClass = 'badge-pez'; 
            icon = '🐟'; 
        } else if (breedLower.includes('tortuga') || breedLower.includes('iguana') || breedLower.includes('lagarto') || breedLower.includes('reptil')) { 
            badgeClass = 'badge-reptil'; 
            icon = '🦎'; 
        } else if (breedLower.includes('cerdo') || breedLower.includes('mini pig') || breedLower.includes('puerquito')) { 
            badgeClass = 'badge-cerdo'; 
            icon = '🐷'; 
        }

        return `
            <div class="pet-list-item">
                <div class="pet-list-left">
                    <div class="pet-list-icon">${icon}</div>
                    <div class="pet-list-info">
                        <h3>${pet.nombre}</h3>
                        <p><span class="pet-tag ${badgeClass}">${pet.raza}</span>${pet.edad} años</p>
                    </div>
                </div>
                <button class="btn-adopt" onclick="openAdoptionModal(${pet.id_mascota}, '${pet.nombre.replace(/'/g, "\\'")}')">Adoptar</button>
            </div>
        `;
    }).join('');
}

// --- 3. GESTIÓN DEL MODAL DINÁMICO ---
function openAdoptionModal(petId, petName) {
    document.getElementById('modal-pet-id').value = petId;
    document.getElementById('modal-pet-name').innerText = petName;
    document.getElementById('adoptionModal').classList.add('show-modal');
}

function closeModal() {
    document.getElementById('adoptionModal').classList.remove('show-modal');
    document.getElementById('form-adoption-request').reset();
}

function setupModalListeners() {
    document.getElementById('btn-close-modal').addEventListener('click', closeModal);

    window.addEventListener('click', (event) => {
        const modal = document.getElementById('adoptionModal');
        if (event.target === modal) {
            closeModal();
        }
    });
}

// --- 4. ENVÍO DE POSTULACIÓN A LA API (POST) ---
function setupFormSubmit() {
    document.getElementById('form-adoption-request').addEventListener('submit', async function (e) {
        e.preventDefault();

        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.disabled = true;

        const requestPayload = {
            id_cliente: sesionActual.idCliente,
            id_mascota: parseInt(document.getElementById('modal-pet-id').value, 10),
            motivo: document.getElementById('req-reason').value,
            espacio: document.getElementById('req-space').value,
            horas: document.getElementById('req-hours').value,
            otra_mascota: document.getElementById('req-other-pets').value,
        };

        try {
            const response = await fetch(`${API_BASE_URL}/solicitudes/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestPayload),
            });

            const data = await response.json();

            if (response.ok) {
                alert('¡Tu solicitud ha sido enviada con éxito! Puedes ver su estado en "Mis solicitudes".');
                closeModal();
                fetchAvailablePets();
            } else {
                alert(data.detail || 'Hubo un inconveniente al procesar tu postulación. Inténtalo de nuevo.');
            }
        } catch (error) {
            console.error('Error al enviar la postulación:', error);
            alert('Error de conexión con el servidor.');
        } finally {
            submitBtn.disabled = false;
        }
    });
}
