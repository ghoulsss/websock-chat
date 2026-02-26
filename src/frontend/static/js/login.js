const API_URL = "http://127.0.0.1:8000";

document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Ошибка авторизации");
            return;
        }

        localStorage.setItem("users_access_token", data.access_token);
        window.location.href = "chat.html";

    } catch (err) {
        console.error(err);
        alert("Ошибка сервера");
    }
});