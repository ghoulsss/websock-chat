import { useState } from "react";
import { register } from "../api/auth";
import type { RegisterRequest, User } from "../types/auth";

interface Props {
  onAuth: (accessToken: string, user: User) => void; // поменяли
}

export default function Register({ onAuth }: Props) {
  const [form, setForm] = useState<RegisterRequest>({
    email: "",
    password: "",
    password_check: "",
    name: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      const data = await register(form);

      // Сохраняем access_token вместо token
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));

      onAuth(data.access_token, data.user);
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <div>
      <h2>Регистрация</h2>

      <input
        name="name"
        placeholder="Имя"
        onChange={handleChange}
      />

      <input
        name="email"
        placeholder="Email"
        onChange={handleChange}
      />

      <input
        type="password"
        name="password"
        placeholder="Пароль"
        onChange={handleChange}
      />

      <input
        type="password"
        name="password_check"
        placeholder="Повторите пароль"
        onChange={handleChange}
      />

      <button onClick={handleSubmit}>
        Зарегистрироваться
      </button>
    </div>
  );
}