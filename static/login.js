if (localStorage.getItem("token")) {
  window.location.href = "/consulta";
}

document
  .getElementById("loginBtn")
  .addEventListener("click", async function () {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const msg = document.getElementById("loginMsg");

    if (!username || !password) {
      msg.textContent = "Por favor, completa todos los campos.";
      return;
    }

    try {
      const response = await fetch(
        "https://loginapi-efcefzbjctcrbcax.canadacentral-01.azurewebsites.net/login",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        }
      );

      const data = await response.json();

      if (response.ok && data.token) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("username", username);
        msg.style.color = "green";
        msg.textContent = "Login exitoso. Redirigiendo...";
        setTimeout(() => {
          window.location.href = "/consulta";
        }, 1000);
      } else {
        msg.style.color = "red";
        msg.textContent = data.error || "Usuario o contraseña incorrectos";
      }
    } catch (error) {
      msg.style.color = "red";
      msg.textContent = "Error de conexión con el servidor.";
    }
  });