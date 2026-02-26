const API_URL = "http://127.0.0.1:8000";

document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const name = document.getElementById("name").value;
    const password = document.getElementById("password").value;
    const password_check = document.getElementById("password_check").value;

    if (password !== password_check) {
        alert("Пароли не совпадают");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, name, password, password_check })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Ошибка регистрации");
            return;
        }

        localStorage.setItem("users_access_token", data.access_token);
        window.location.href = "chat.html";

    } catch (err) {
        console.error(err);
        alert("Ошибка сервера");
    }
});