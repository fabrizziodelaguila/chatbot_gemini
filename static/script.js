document.getElementById("enviar").addEventListener("click", async function () {
    let input = document.getElementById("pregunta").value;

    let response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ categoria: input })
    });

    let data = await response.json();
    document.getElementById("respuesta").innerText = data.respuesta_gemini || JSON.stringify(data);
});
