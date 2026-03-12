import { useState } from "react";
import { login } from "../api/auth";
import type { LoginRequest, User } from "../types/auth";

interface Props {
  onAuth: (accessToken: string, user: User) => void;
}

export default function Login({ onAuth }: Props) {
  const [form, setForm] = useState<LoginRequest>({
    email: "",
    password: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      const data = await login(form);

      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));

      onAuth(data.access_token, data.user);
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <div>
      <h2>Вход</h2>

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

      <button onClick={handleSubmit}>Войти</button>
    </div>
  );
}