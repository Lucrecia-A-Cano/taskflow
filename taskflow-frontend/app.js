const API_URL = "http://127.0.0.1:8000/api";
let accessToken = null;

function authHeaders() {
  return { Authorization: `Bearer ${accessToken}` };
}

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const response = await fetch(`${API_URL}/token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    document.getElementById("login-error").textContent =
      response.status === 429
        ? "Demasiados intentos. Esperen un minuto."
        : "Usuario o contraseña incorrectos.";
    return;
  }

  const data = await response.json();
  accessToken = data.access;
  document.getElementById("login-box").style.display = "none";
  document.getElementById("app-box").style.display = "block";
  loadProjects();
  loadTasks();
}

async function loadProjects() {
  const response = await fetch(`${API_URL}/projects/`, { headers: authHeaders() });
  const data = await response.json();
  const select = document.getElementById("project");
  select.innerHTML = "";
  data.results.forEach((project) => {
    const option = document.createElement("option");
    option.value = project.id;
    option.textContent = project.name;
    select.appendChild(option);
  });
}

async function loadTasks() {
  const response = await fetch(`${API_URL}/tasks/`, { headers: authHeaders() });
  const data = await response.json();
  const list = document.getElementById("tasks");
  list.innerHTML = "";
  data.results.forEach((task) => {
    const li = document.createElement("li");
    li.textContent = `${task.title} — ${task.status}`;
    list.appendChild(li);
  });
}

async function createTask() {
  const title = document.getElementById("new-title").value;
  const project = document.getElementById("project").value;
  const errorBox = document.getElementById("app-error");
  errorBox.textContent = "";
  if (!title || !project) return;

  const response = await fetch(`${API_URL}/tasks/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ title, project: Number(project) }),
  });

  if (!response.ok) {
    const data = await response.json();
    errorBox.textContent = JSON.stringify(data.detail);
    return;
  }

  document.getElementById("new-title").value = "";
  loadTasks();
}
