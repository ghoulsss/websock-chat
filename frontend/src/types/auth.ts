export interface User {
  id: number;
  email: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  password_check: string;
  name: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

export interface Message {
  id: number;
  user_id: number;
  name: string;
  content: string;
  created_at: string;
}