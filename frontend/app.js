const API = "https://<TU-API>.fly.dev";  // actualiza con tu URL de Fly.io

const video = document.getElementById("cam");
const canvas = document.getElementById("canvas");
const snap  = document.getElementById("snap");
const result= document.getElementById("result");

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => video.srcObject = stream);

snap.onclick = async () => {
  // 1) Captura frame
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);

  // 2) Convierte a blob
  const blob = await new Promise(r => canvas.toBlob(r, "image/jpeg"));

  // 3) Envia a /predict
  const form = new FormData();
  form.append("file", blob, "foto.jpg");
  const resp = await fetch(`${API}/predict`, { method: "POST", body: form });
  const { label, confidence } = await resp.json();

  // 4) Muestra resultado
  result.innerHTML = `
    <h2>Predicción: ${label} (${(confidence*100).toFixed(1)}%)</h2>
    <button id="yes">👍 Correcto</button>
    <button id="no">👎 Incorrecto</button>
  `;

  // 5) Feedback
  document.getElementById("yes").onclick = () => sendFeedback(label, label);
  document.getElementById("no").onclick  = () => {
    const correct = prompt("¿Cuál es la etiqueta correcta? (Reciclable / No reciclable)");
    if (correct) sendFeedback(label, correct);
  };
};

async function sendFeedback(predicted, correct) {
  await fetch(`${API}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ predicted, correct })
  });
  alert("¡Gracias por tu feedback! 💚");
}
