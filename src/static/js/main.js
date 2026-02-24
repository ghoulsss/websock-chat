console.log("main.js загружен");

// ====================
// Переключение вкладок
// ====================

document.querySelectorAll(".tab").forEach((tab) => {
	tab.addEventListener("click", () => showTab(tab.dataset.tab));
});

function showTab(tabName) {
	document
		.querySelectorAll(".tab")
		.forEach((tab) => tab.classList.remove("active"));

	document
		.querySelectorAll(".form")
		.forEach((form) => form.classList.remove("active"));

	document
		.querySelector(`.tab[data-tab="${tabName}"]`)
		.classList.add("active");

	document
		.getElementById(`${tabName}Form`)
		.classList.add("active");
}

// ====================
// Валидация
// ====================

const validateForm = (fields) =>
	fields.every((field) => field.trim() !== "");

// ====================
// Отправка запроса
// ====================

const sendRequest = async (url, data) => {
	try {
		const response = await fetch(url, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(data),
		});

		const result = await response.json();

		if (!response.ok) {
			alert(result.message || "Ошибка!");
			return null;
		}

		return result;
	} catch (error) {
		console.error(error);
		alert("Ошибка сервера");
		return null;
	}
};

// ====================
// Login
// ====================

document
	.getElementById("loginForm")
	.addEventListener("submit", async (event) => {
		event.preventDefault();

		const email = document.querySelector(
			'#loginForm input[type="email"]'
		).value;

		const password = document.querySelector(
			'#loginForm input[type="password"]'
		).value;

		if (!validateForm([email, password])) {
			alert("Заполните все поля");
			return;
		}

		const data = await sendRequest("/login", {
			email,
			password,
		});

		if (data) {
			window.location.href = "/chat/";
		}
	});

// ====================
// Register
// ====================

document
	.getElementById("registerForm")
	.addEventListener("submit", async (event) => {
		event.preventDefault();

		const email = document.querySelector(
			'#registerForm input[type="email"]'
		).value;

		const name = document.querySelector(
			'#registerForm input[type="text"]'
		).value;

		const passwords = document.querySelectorAll(
			'#registerForm input[type="password"]'
		);

		const password = passwords[0].value;
		const password_check = passwords[1].value;

		if (!validateForm([email, name, password, password_check])) {
			alert("Заполните все поля");
			return;
		}

		if (password !== password_check) {
			alert("Пароли не совпадают");
			return;
		}

		await sendRequest("/register", {
			email,
			name,
			password,
			password_check,
		});
	});
