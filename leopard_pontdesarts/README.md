### **🚀 Leopard Pont Des Arts API**
A FastAPI-based service leveraging CrewAI and a Large Language Model (LLM) for intelligent responses. Supports both **local development** and **Podman-based deployments**.

---

## **📌 Features**
✅ **LLM Integration** – Uses an external LLM API  
✅ **FastAPI-based REST API** – Easily extendable endpoints  
✅ **Environment Config Support** – Works with `.env` or Kubernetes `ConfigMap`  
✅ **Podman Desktop Deployment** – Ready for local and containerized execution

---

## **🛠️ Setup Instructions**

### **1️⃣ Local Development (Without Podman)**
#### **🔹 Prerequisites**
- **Python 3.11+**
- **pip & virtualenv**

#### **🔹 Install & Run**
```bash
# Clone the repository
git clone https://github.com/your-repo/leopard_pontdesarts.git
cd leopard_pontdesarts

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate      # For Windows

# Install dependencies
pip install -r requirements.txt

# Create a `.env` file with your API credentials
cp .env.example .env
nano .env  # Update API keys

# Run the API locally
python -m src.main --mode api
```

#### **🔹 Test the API**
```bash
curl -X GET http://127.0.0.1:8000/
curl -X GET http://127.0.0.1:8000/leopard-crossing
```

---

### **2️⃣ Run with Podman**
#### **🔹 Prerequisites**
- **[Podman Installed](https://podman.io/getting-started/installation)**
- **Podman Desktop (Optional, for GUI management)**

#### **🔹 Build & Run with Podman**
```bash
# Build the container
podman build -t quay.io/yourusername/leopard_pontdesarts:latest .

# Run the container with environment variables
podman run --env-file .env -p 8000:8000 quay.io/yourusername/leopard_pontdesarts:latest
```

---

### **3️⃣ Deploy via Podman Desktop (Kube YAML)**
#### **🔹 Steps**
1. **Create the Pod & ConfigMap** using the provided `pod.yaml`
2. **Apply YAML in Podman Desktop**
   ```bash
   podman kube play pod.yaml
   ```
3. **Check Running Containers**
   ```bash
   podman ps -a
   ```

#### **🔹 Access the API**
```bash
curl -X GET http://localhost:8000/
curl -X GET http://localhost:8000/leopard-crossing
```

---

## **📄 API Endpoints**
| Method | Endpoint                   | Description                         |
|--------|----------------------------|-------------------------------------|
| GET    | `/`                        | API health check                   |
| GET    | `/leopard-crossing`        | Get raw LLM response               |
| GET    | `/leopard-crossing-ui`     | Get formatted response via service |

---

## **📦 Environment Configuration**
The app reads values from `.env` or a `ConfigMap`.

### **✅ `.env` Example**
```ini
LLM_BASE_URL="https://your-llm-api.com"
LLM_MODEL="your-llm-model"
LLM_API_KEY="your-secret-key"  # Replace with actual key
FORMATTER_API_URL="http://localhost:8001/process"
CHROMA_DB_PATH="/opt/app-root/src/.local/chroma_db"
LOG_LEVEL="INFO"
```

### **✅ `ConfigMap` Equivalent (for Kubernetes/Podman)**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: leopard-config
data:
  LLM_BASE_URL: "https://your-llm-api.com"
  LLM_MODEL: "your-llm-model"
  LLM_API_KEY: "your-secret-key"
  FORMATTER_API_URL: "http://localhost:8001/process"
  CHROMA_DB_PATH: "/opt/app-root/src/.local/chroma_db"
  LOG_LEVEL: "INFO"
```

---

## **🚀 Troubleshooting**
### **Port Not Accessible?**
- Ensure **`hostPort: 8000`** is set in `pod.yaml`
- Check running containers:
  ```bash
  podman ps -a
  ```

### **LLM API Errors?**
- Verify `.env` or `ConfigMap` **has correct API key**
- Run:
  ```bash
  podman logs leopard-crossing-api
  ```

---

## **🎯 Summary**
| Mode               | Command |
|--------------------|---------|
| **Local (No Podman)** | `python -m src.main --mode api` |
| **Podman CLI** | `podman run --env-file .env -p 8000:8000 quay.io/yourusername/leopard_pontdesarts:latest` |
| **Podman Desktop (Kube)** | `podman kube play pod.yaml` |

---
