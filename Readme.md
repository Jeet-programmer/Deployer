# 🛠️ Universal Dockerfile Generator

A full-stack AI-powered platform that generates `Dockerfile`s for any public GitHub repository. Built with **FastAPI** as the backend and **Streamlit** as the user-friendly frontend, this tool intelligently analyze projects and suggest containerization strategies.

---

## 🚀 Features

- 🔗 Submit any **public GitHub repo URL**
- 🤖 AI-generated **Dockerfile** for projects in Python, Node.js, Java, C++, etc.
- 📦 FastAPI backend and Streamlit frontend
- 📄 Optional fields (coming soon): build/run commands, Docker Compose support

---

## 📁 Project Structure

```

universal-dockerfile-generator/
├── app.py              # FastAPI backend (API to clone repo + call AI)
├── main.py             # Streamlit frontend (UI interface)
├── gemini\_agent.py     # AI agent using GPT-4o-mini via HTTP API
├── requirements.txt    # All Python dependencies
├── Dockerfile          # Builds and runs both backend and frontend
└── README.md           # This file

````

---

## 🧠 How It Works

1. **Clone** the GitHub repo submitted by the user.
2. **Extract & summarize** important files like `main.py`, `package.json`, `requirements.txt`, etc.
3. **Send summary** to an AI model with a prompt to generate a Dockerfile.
4. **Return** the Dockerfile in the Streamlit UI.

---

## 🧰 Tech Stack

- ⚙️ **FastAPI** — REST API backend
- 🖼️ **Streamlit** — Frontend UI
- 🧠 **GPT-4o-mini** — DevScript Chat API (AI generation)
- 🐳 **Docker** — Containerized deployment

---

## 🐳 Dockerfile

```dockerfile
# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI (8000) and Streamlit (8051)
EXPOSE 8000
EXPOSE 8051

# Launch both services, prioritize Streamlit on port 8051
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run main.py --server.port=8051 --server.address=0.0.0.0"]
````

---

## 📦 `requirements.txt`

```txt
fastapi
streamlit
uvicorn
requests
pydantic
```

Install manually:

```bash
pip install -r requirements.txt
```

---

## 🧪 Run Locally

### Clone the Repository

```bash
git clone https://github.com/yourusername/universal-dockerfile-generator.git
cd universal-dockerfile-generator
```

### Build the Docker Image

```bash
docker build -t dockerfile-generator .
```

### Run the Container

```bash
docker run -p 8051:8051 -p 8000:8000 dockerfile-generator
```

Visit:

* 🌐 [http://localhost:8051](http://localhost:8051) → Streamlit (Main UI)
* 📄 [http://localhost:8000/docs](http://localhost:8000/docs) → FastAPI Docs

---

## 📤 API Reference

### `POST /generate`

**Body**:

```json
{
  "git_url": "https://github.com/user/project"
}
```

**Response**:

```json
{
  "deployment_file": "FROM python:3.11\n..."
}
```

---

## 🛣 Roadmap

* [x] Dockerfile generation
* [ ] Docker Compose file generation
* [ ] Custom build & run command support
* [ ] Download button in UI
* [ ] Private GitHub repo support via token

---

## 🧑‍💻 Author

Built with ❤️ by [Jeet Ghosh](https://github.com/Jeet-programmer)

---

## 🪪 License

MIT License — use freely, modify openly, contribute back 🙌

