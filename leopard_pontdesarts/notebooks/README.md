
# 🚀 CrewAI Learning Journey: From Basics to OpenShift Deployment

This repository provides a **structured learning path** for mastering **CrewAI**, starting from a simple AI agent to a **production-ready deployment on OpenShift**.

## 📌 Learning Flow

| Level  | Description |
|--------|------------|
| **090-Level** | 🟢 Beginner: Minimal setup using OpenAI's GPT-4o |
| **100-Level** | 🔵 Configuration & LLM Portability (Env Variables & Config) |
| **200-Level** | 🟣 Multi-Agent Collaboration & Debugging |
| **300-Level** | 🔴 Response Formatting & FastAPI Deployment |
| **400-Level** | 🚀 OpenShift Deployment & API Exposure |

---

## 🏗 **Setup Instructions**

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/rrbanda/crewai-examples.git
cd crewai-examples/leopard_pontdesarts/notebooks
```

### 2️⃣ **Install Dependencies**
Ensure you have Python 3.10+ installed, then run:
```sh
pip install -r requirements.txt
```

### 3️⃣ **Run the Notebooks**
```sh
jupyter notebook
```
Now, open the **notebooks** folder and follow the structured learning path.

---

## 📜 **Notebook Guide**

### 🟢 **090-Level: Beginner Example**
- Introduces **CrewAI**
- Runs a **single AI agent** with OpenAI's **GPT-4o**
- Executes a minimal setup with `python leopard-pont-des-arts.py`

📌 **Run:** _No external configuration needed._

---

### 🔵 **100-Level: Configuration & LLM Portability**
- Loads **API keys & URLs** via `.env` & `config.yaml`
- Supports **multiple LLMs** (OpenAI, local models, RHOAI)
- Introduces structured **YAML-based config management**

📌 **Run:** _Requires setting up `config.yaml` and `.env`._

---

### 🟣 **200-Level: Multi-Agent Collaboration & Debugging**
- Implements **multiple AI agents** with **CrewAI**
- Enables **debugging** and **inter-agent collaboration**
- Introduces **Crew & Task management** concepts

📌 **Run:** _Executes CrewAI agents in sequence._

---

### 🔴 **300-Level: Response Formatting & FastAPI Deployment**
- Formats AI responses as **JSON or Markdown**
- Deploys a **FastAPI-based microservice**
- Containerized with **Podman/Docker**

📌 **Run:**
```sh
podman build -t crewai-api:latest .
podman run -p 8000:8000 crewai-api:latest
```

---

### 🚀 **400-Level: OpenShift Deployment**
- Deploys the **CrewAI FastAPI service** to OpenShift
- Uses **Kubernetes pods** with **ConfigMaps**
- Ensures **scalability & cloud readiness**

📌 **Run:**
```sh
oc apply -f openshift/pod.yaml
```

---

## 📦 **Deployment Options**
| Deployment | Method |
|------------|--------|
| **Local** | `python leopard-pont-des-arts.py` |
| **FastAPI (Podman/Docker)** | `podman run -p 8000:8000 crewai-api:latest` |
| **OpenShift** | `oc apply -f openshift/pod.yaml` |

---

## 🤝 Contributing
We welcome **issues, PRs, and discussions** to improve this repo! 🚀

---

📌 **Maintained by:** [@rrbanda](https://github.com/rrbanda)
```

