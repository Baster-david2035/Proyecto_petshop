document.addEventListener('DOMContentLoaded', () => {
    const recoveryForm = document.getElementById('recoveryDirectForm');
    const passwordInput = document.getElementById('new-password');
    const togglePasswordBtn = document.getElementById('toggleNewPassword');
    const successMessage = document.getElementById('recovery-success-message');
    const btnSubmit = document.getElementById('btnRecoverySubmit');
    const btnText = document.getElementById('btn-recovery-text');
    const btnSpinner = document.getElementById('btn-recovery-spinner');

    let errorMessage = document.getElementById('recovery-error-message');
    if (!errorMessage) {
        errorMessage = document.createElement('div');
        errorMessage.id = 'recovery-error-message';
        errorMessage.className = 'login-toast-error';
        errorMessage.style.display = 'none';
        successMessage.parentNode.insertBefore(errorMessage, successMessage);
    }

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

    // 2. Recuperar
    recoveryForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        successMessage.style.display = 'none';
        errorMessage.style.display = 'none';
        setLoading(true);

        const payload = {
            correo: document.getElementById('recovery-email').value.trim(),
            nueva_contrasena: passwordInput.value,
        };

        try {
            const res = await fetch(`${API_BASE_URL}/usuarios/recuperar`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || 'No se pudo actualizar la contraseña.');
            }

            setLoading(false);
            successMessage.style.display = 'block';
            recoveryForm.reset();

            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);

        } catch (error) {
            setLoading(false);
            errorMessage.innerText = `⚠️ ${error.message}`;
            errorMessage.style.display = 'block';
        }
    });
});
