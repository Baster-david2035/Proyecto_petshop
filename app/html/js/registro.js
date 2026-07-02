document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const passwordInput = document.getElementById('password');
    const togglePasswordBtn = document.getElementById('toggleRegisterPassword');
    const successMessage = document.getElementById('register-success-message');
    const btnSubmit = document.getElementById('btnRegisterSubmit');
    const btnText = document.getElementById('btn-register-text');
    const btnSpinner = document.getElementById('btn-register-spinner');

    // Si no existe un cuadro de error en el HTML, lo creamos dinamicamente
    let errorMessage = document.getElementById('register-error-message');
    if (!errorMessage) {
        errorMessage = document.createElement('div');
        errorMessage.id = 'register-error-message';
        errorMessage.className = 'login-toast-error';
        errorMessage.style.display = 'none';
        successMessage.parentNode.insertBefore(errorMessage, successMessage);
    }

    // 1. Mostrar / Ocultar Contraseña de forma segura
    togglePasswordBtn.addEventListener('click', function (e) {
        e.preventDefault();
        const isPassword = passwordInput.getAttribute('type') === 'password';
        passwordInput.setAttribute('type', isPassword ? 'text' : 'password');
        this.innerText = isPassword ? '🙈' : '👁';
    });

    function setLoading(isLoading) {
        if (isLoading) {
            btnSubmit.setAttribute('disabled', 'true');
            btnSubmit.style.opacity = '0.8';
            btnText.style.display = 'none';
            btnSpinner.style.display = 'inline-block';
        } else {
            btnSubmit.removeAttribute('disabled');
            btnSubmit.style.opacity = '1';
            btnText.style.display = 'inline-block';
            btnSpinner.style.display = 'none';
        }
    }

    // 2. Registro real
    registerForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        successMessage.style.display = 'none';
        errorMessage.style.display = 'none';
        setLoading(true);

        const payload = {
            nombre: document.getElementById('name').value.trim(),
            telefono: document.getElementById('phone').value.trim(),
            correo: document.getElementById('email').value.trim(),
            contrasena: passwordInput.value,
        };

        try {
            const res = await fetch(`${API_BASE_URL}/usuarios/registro`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || 'No se pudo completar el registro.');
            }

            setLoading(false);
            successMessage.style.display = 'block';
            registerForm.reset();

            setTimeout(() => {
                window.location.href = 'login.html';
            }, 1800);

        } catch (error) {
            setLoading(false);
            errorMessage.innerText = `⚠️ ${error.message}`;
            errorMessage.style.display = 'block';
        }
    });
});
