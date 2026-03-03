import { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Chat from "./pages/Chat";
import type { User } from "./types/auth";

function App() {
  const [accessToken, setAccessToken] = useState<string | null>(
    localStorage.getItem("access_token")
  );

  const [user, setUser] = useState<User | null>(
    localStorage.getItem("user")
      ? JSON.parse(localStorage.getItem("user")!)
      : null
  );

  const [isRegister, setIsRegister] = useState(false);

  const handleAuth = (accessToken: string, user: User) => {
    setAccessToken(accessToken);
    setUser(user);

    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("user", JSON.stringify(user));
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    setAccessToken(null);
    setUser(null);
  };

  if (!accessToken || !user) {
    return isRegister ? (
      <>
        <Register onAuth={handleAuth} />
        <p onClick={() => setIsRegister(false)}>
          Уже есть аккаунт?
        </p>
      </>
    ) : (
      <>
        <Login onAuth={handleAuth} />
        <p onClick={() => setIsRegister(true)}>
          Нет аккаунта?
        </p>
      </>
    );
  }

  return (
    <Chat token={accessToken} user={user} onLogout={logout} />
  );
}

export default App;