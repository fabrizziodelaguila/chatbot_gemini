document.getElementById("registerBtn").addEventListener("click", async function () {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const msg = document.getElementById("registerMsg");

    if (!username || !password) {
        msg.textContent = "Por favor, completa todos los campos.";
        msg.style.color = "red";
        return;
    }

    try {
        const response = await fetch("https://loginapi-efcefzbjctcrbcax.canadacentral-01.azurewebsites.net/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            msg.style.color = "green";
            msg.textContent = "Registro exitoso. Ahora puedes iniciar sesión.";
            setTimeout(() => {
                window.location.href = "login.html";
            }, 1500);
        } else {
            msg.style.color = "red";
            msg.textContent = data.error || "No se pudo registrar.";
        }
    } catch (error) {
        msg.style.color = "red";
        msg.textContent = "Error de conexión con el servidor.";
    }
});