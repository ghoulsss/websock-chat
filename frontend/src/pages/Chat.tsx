import { useEffect, useState, useRef } from "react";
import type { Message, User } from "../types/auth";

interface Props {
  token: string;
  user: User;
  onLogout: () => void;
}

export default function Chat({ token, user, onLogout }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!token) return;
    
    const ws = new WebSocket(`ws://localhost:8000/ws/chat?access_token=${token}`);

    ws.onopen = () => console.log("WebSocket connected");
    ws.onmessage = (event) => console.log("Message:", event.data);
    ws.onclose = (event) => console.log("WebSocket closed", event.code);
    ws.onerror = (err) => console.error("WebSocket error", err);
    
    ws.onmessage = (event) => {
      try {
        const data: Message = JSON.parse(event.data);
        setMessages((prev) => [...prev, data]);
      } catch (err) {
        console.error("Error parsing message:", err);
      }
    };
    socketRef.current = ws;

    return () => {
      ws.close();
    };
  }, [token]);

  const sendMessage = () => {
    if (!socketRef.current || !input.trim()) return;
    socketRef.current.send(JSON.stringify({ content: input }));
    setInput("");
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto" }}>
      <h2>Чат</h2>
      <p>Вы вошли как: {user.email}</p>
      <button onClick={onLogout}>Выйти</button>

      <div
        style={{
          border: "1px solid #ccc",
          height: 400,
          overflowY: "auto",
          padding: 10,
          marginTop: 10,
        }}
      >
        {messages.map((msg) => (
          <div
            key={msg.id}
            style={{
              marginBottom: 10,
              padding: 8,
              background: msg.user_id === user.id ? "#0037ff" : "#e6126e",
            }}
          >
            <strong>{msg.name}</strong>
            <div>{msg.content}</div>
            <small>{new Date(msg.created_at).toLocaleTimeString()}</small>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 10 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ width: "80%" }}
        />
        <button onClick={sendMessage}>Отправить</button>
      </div>
    </div>
  );
}