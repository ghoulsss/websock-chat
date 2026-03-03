import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
} from "../types/auth";

const BASE_URL = "http://localhost:8000";

export async function login(
  data: LoginRequest
): Promise<AuthResponse> {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Неверный email или пароль");
  }

  return response.json();
}

export async function register(
  data: RegisterRequest
): Promise<AuthResponse> {
  const response = await fetch(`${BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Ошибка регистрации");
  }

  return response.json();
}