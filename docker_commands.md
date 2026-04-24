# 🐳 Docker Basic Commands (Cheat Sheet)

## 📦 1. Image related

### 🔍 Image list dekha

```bash
docker images
```

### 📥 Docker Hub theke image ana

```bash
docker pull ubuntu
docker pull python:3.10
```

### ❌ Image delete

```bash
docker rmi image_name
```

---

## 🚀 2. Container run & control

### ▶️ Container run

```bash
docker run hello-world
```

### 🧠 Interactive mode (bash e dhukar jonno)

```bash
docker run -it ubuntu bash
```

### 📋 Running container dekha

```bash
docker ps
```

### 📋 Sob container (stopped + running)

```bash
docker ps -a
```

### ⛔ Container stop

```bash
docker stop container_id
```

### ▶️ Stop kora container abar start

```bash
docker start container_id
```

### 🗑️ Container delete

```bash
docker rm container_id
```

---

## 🧱 3. Build & Push (important)

### 🏗️ Image build (Dockerfile theke)

```bash
docker build -t my-app .
```

### 🏷️ Tag (Docker Hub er jonno)

```bash
docker tag my-app username/my-app:latest
```

### 🔐 Login

```bash
docker login
```

### 📤 Push to Docker Hub

```bash
docker push username/my-app
```

---

## 🔍 4. Debug & inspect

### 🧾 Logs dekha

```bash
docker logs container_id
```

### 🔎 Container details

```bash
docker inspect container_id
```

---

## 🌐 5. Port mapping (VERY IMPORTANT)

```bash
docker run -p 8000:8000 my-app
```

👉 format:

```text
host_port : container_port
```

---

## 📁 6. Volume (data save)

```bash
docker run -v /host/path:/container/path image
```

---

## 🧹 7. Cleanup (useful)

### ❌ All stopped container remove

```bash
docker container prune
```

### ❌ All unused image remove

```bash
docker image prune
```

---

# 🎯 Mini workflow (real use)

```bash
docker pull python:3.10
docker run -it python:3.10 bash
```

OR

```bash
docker build -t my-app .
docker run -p 8000:8000 my-app
docker push username/my-app
```

---

# 🧠 Mental Model

| Concept    | Meaning           |
| ---------- | ----------------- |
| Image      | Template          |
| Container  | Running instance  |
| Dockerfile | Build instruction |
| Docker Hub | Image storage     |

---

# 🚀 Next (important for you)

Tumi ekhon ready for:

👉 FastAPI + Docker
👉 ML model deployment
👉 End-to-end system

---

💬 bolo:
👉 “Dockerfile sikhte chai”
👉 “ML project dockerize korbo”

Ami next level e niye jabo 🚀
