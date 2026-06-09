const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user).token : null;
}

function authHeaders() {
  const token = getToken();
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

// --- AUTH ---
export async function registerUser(username: string, password: string, is_creator: number) {
  const res = await fetch(`${API_URL}/users/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password, is_creator }),
  });
  if (!res.ok) throw new Error((await res.json()).detail);
  return res.json();
}

export async function loginUser(username: string, password: string) {
  const res = await fetch(`${API_URL}/users/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error((await res.json()).detail);
  return res.json();
}

// --- PUZZLES ---
export async function getPuzzles(params?: Record<string, string | number>) {
  const query = params ? "?" + new URLSearchParams(params as Record<string, string>).toString() : "";
  const res = await fetch(`${API_URL}/puzzles/${query}`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Failed to fetch puzzles");
  return res.json();
}

export async function getMyPuzzles() {
  const res = await fetch(`${API_URL}/puzzles/my_puzzles`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Failed to fetch your puzzles");
  return res.json();
}

export async function getPuzzle(id: number) {
  const res = await fetch(`${API_URL}/puzzles/${id}`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Puzzle not found");
  return res.json();
}

export async function createPuzzle(data: {
  title: string;
  hor_size: number;
  ver_size: number;
  solution_grid: number[][];
}) {
  const res = await fetch(`${API_URL}/puzzles/`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error((await res.json()).detail);
  return res.json();
}

export async function updatePuzzle(id: number, data: Partial<{ title: string; hor_size: number; ver_size: number; solution_grid: number[][] }>) {
  const res = await fetch(`${API_URL}/puzzles/${id}`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error((await res.json()).detail);
  return res.json();
}

export async function deletePuzzle(id: number) {
  const res = await fetch(`${API_URL}/puzzles/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to delete puzzle");
  return res.json();
}

// --- ATTEMPTS ---
export async function getAttempts() {
  const res = await fetch(`${API_URL}/attempts/`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Failed to fetch attempts");
  return res.json();
}

export async function getAttempt(id: number) {
  const res = await fetch(`${API_URL}/attempts/${id}`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Attempt not found");
  return res.json();
}

export async function createAttempt(puzzle_id: number) {
  const res = await fetch(`${API_URL}/attempts/`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ puzzle_id }),
  });
  if (!res.ok) throw new Error((await res.json()).detail);
  return res.json();
}

export async function updateAttempt(id: number, current_grid: number[][]) {
  const res = await fetch(`${API_URL}/attempts/${id}`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify({ current_grid }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail ?? "Failed to update attempt");
  }
  return res.json();
}