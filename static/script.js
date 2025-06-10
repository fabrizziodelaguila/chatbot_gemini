const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "login.html";
}

document.getElementById("enviar").addEventListener("click", async function () {
  const input = document.getElementById("pregunta").value;

  const response = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ categoria: input })
  });

  const data = await response.json();
  document.getElementById("respuesta").innerText = data.respuesta_gemini || JSON.stringify(data);
});