document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('mainLoginForm');
    const passwordInput = document.getElementById('password');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const errorMessage = document.getElementById('login-error-message');
    const btnSubmit = document.getElementById('btnLoginSubmit');
    const btnText = document.getElementById('btn-text');
    const btnSpinner = document.getElementById('btn-spinner');

    // 1. Mostrar / Ocultar Contraseña
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

    // 2. Login real contra el backend.
    loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const emailValue = document.getElementById('email').value.trim();
        const passwordValue = passwordInput.value;

        errorMessage.style.display = 'none';
        setLoading(true);

        try {
            const res = await fetch(`${API_BASE_URL}/usuarios/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ correo: emailValue, contrasena: passwordValue }),
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || 'Credenciales inválidas');
            }

            guardarSesion(data);

            if (data.es_admin) {
                window.location.href = 'admin.html';
            } else {
                window.location.href = 'home.html';
            }

        } catch (error) {
            setLoading(false);
            errorMessage.innerText = `⚠️ ${error.message}`;
            errorMessage.style.display = 'block';
        }
    });
});
