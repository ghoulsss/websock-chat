const token = localStorage.getItem("users_access_token");

if (!token) {
    window.location.href = "login.html";
}

// WebSocket
const ws = new WebSocket(`ws://127.0.0.1:8000/ws?token=${token}`);

ws.onopen = () => console.log("WS connected");

ws.onmessage = (event) => {
    const messages = document.getElementById("messages");
    const div = document.createElement("div");
    div.textContent = event.data;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
};

document.getElementById("sendBtn").addEventListener("click", () => {
    const input = document.getElementById("msgInput");
    if(input.value.trim() !== "") {
        ws.send(input.value);
        input.value = "";
    }
});

document.getElementById("logout").addEventListener("click", () => {
    localStorage.removeItem("users_access_token");
    window.location.href = "login.html";
});