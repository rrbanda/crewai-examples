### **📌 Leopard Pont des Arts AI Agent API**

This repository provides an AI-powered agent that computes how long it takes for a leopard to cross the Pont des Arts bridge, with both **raw JSON output** and **UI-friendly formatted output**.

---

## **🚀 Features**
- 🦁 **Leopard Crossing Time Calculation** → Uses an AI agent to compute crossing time.
- 📡 **FastAPI-based REST API** → Exposes easy-to-use API endpoints.
- 🎨 **UI-friendly Response Formatting** → Calls the external **Formatter API** at [`ai-agent-formatter`](https://github.com/rrbanda/ai-agent-formatter/tree/main) to transform responses into UI components.
- 🔧 **Configurable Formatter API** → Loads formatter service URL dynamically from `config.yaml`.

---

## **📂 Folder Structure**
```
leopard_pontdesarts/
│── src/
│   ├── agents.py               # Defines LeopardPontDesArtsAgent
│   ├── tasks.py                # Defines the agent task
│   ├── llm.py                  # Handles LLM API calls
│   ├── api.py                  # FastAPI application
│   ├── config.yaml             # Configurations (Formatter & LLM)
│── configs/
│   ├── agents.yaml             # Agent configuration
│   ├── prompts.yaml            # Prompt configuration
│   ├── tasks.yaml              # Task configuration
│── tests/
│   ├── test_api.py             # Unit tests for API
│── requirements.txt            # Required dependencies
│── README.md                   # This documentation
```

---

## **⚡ Installation & Setup**

### **1️⃣ Clone this repository**
```sh
git clone https://github.com/your-username/leopard_pontdesarts.git
cd leopard_pontdesarts
```

### **2️⃣ Set up virtual environment**
```sh
python -m venv venv
source venv/bin/activate  # On MacOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### **3️⃣ Install dependencies**
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

### **4️⃣ Configure API URLs**
Modify `configs/config.yaml` to define the **Formatter API URL** and **LLM API URL**:
```yaml
llm:
  api_url: "https://deepseek-r1-distill-qwen-14b-maas-apicast-production.apps.prod.rhoai.rh-aiservices-bu.com:443"
  model: "deepseek-r1-distill-qwen-14b"
  api_key: "YOUR_LLM_API_KEY"

formatter:
  api_url: "http://localhost:8001/process"  # ✅ Formatter API URL
```

### **5️⃣ Run the API**
```sh
python -m src.main --mode api
```
The API will start on **`http://0.0.0.0:8000`**.

---

## **📡 API Endpoints**
| **Endpoint** | **Purpose** | **Example Response** |
|-------------|------------|----------------------|
| **`GET /`** | Check if API is running | `{ "message": "Leopard Pont des Arts API is running!" }` |
| **`GET /leopard-crossing`** | Returns **raw JSON** output from AI agent | `{ "time_seconds": 9.62, "explanation": "..." }` |
| **`GET /leopard-crossing-ui`** | Returns **formatted UI response** via external formatter | `{ "ui_type": "table", "content": [...] }` |

---

## **🖼️ Example API Calls**
### **Raw JSON Response**
```sh
curl -X GET "http://localhost:8000/leopard-crossing"
```
**Response:**
```json
{
  "time_seconds": 9.62,
  "explanation": "The leopard's speed is converted from 58 km/h to 16.111 m/s. The time to cross 155 meters is 155 / 16.111 ≈ 9.62 sec."
}
```

### **UI-Friendly Response**
```sh
curl -X GET "http://localhost:8000/leopard-crossing-ui"
```
**Response from Formatter:**
```json
{
  "ui_type": "table",
  "content": [
    { "key": "time_seconds", "value": 9.62 },
    { "key": "explanation", "value": "The leopard runs at 58 km/h, converted to 16.111 m/s. The crossing time is 155m / 16.111 m/s ≈ 9.62 sec." }
  ]
}
```

---

## **🔗 Running the Formatter API**
Before calling `/leopard-crossing-ui`, **ensure the Formatter API** is running.  
The Formatter API is available at [`ai-agent-formatter`](https://github.com/rrbanda/ai-agent-formatter/tree/main).

### **Steps to Run the Formatter API**
1. **Clone the formatter repository**:
   ```sh
   git clone https://github.com/rrbanda/ai-agent-formatter.git
   cd ai-agent-formatter
   ```

2. **Set up and run the API**:
   ```sh
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
   ```

3. **Verify it’s running**:
   ```sh
   curl -X POST "http://localhost:8001/process" \
   -H "Content-Type: application/json" \
   -d '{"format": "json", "data": {"time_seconds": 9.62, "explanation": "The leopard runs at 58 km/h, converted to 16.111 m/s. The crossing time is 155m / 16.111 m/s ≈ 9.62 sec."}}'
   ```
   **Expected Response:**
   ```json
   {
     "ui_type": "table",
     "content": [
       { "key": "time_seconds", "value": 9.62 },
       { "key": "explanation", "value": "The leopard runs at 58 km/h, converted to 16.111 m/s. The crossing time is 155m / 16.111 m/s ≈ 9.62 sec." }
     ]
   }
   ```

---

## **🛠️ Running Tests**
Run unit tests to ensure everything works:
```sh
pytest tests/
```

---

## **🚀 Next Steps**
- 🛠️ **Integrate UI** → Use `/leopard-crossing-ui` for a frontend-friendly response.
- 📊 **Add support for Markdown Output** → Extend the Formatter API to handle `markdown` responses.
- 🌍 **Deploy API** → Run on **AWS Lambda**, **OpenShift**, or **Docker**.

---

## **📌 Credits**
- **LLM & AI Agent** → [`crewai`](https://github.com/joaomdmoura/crewai)
- **UI Formatter** → [`ai-agent-formatter`](https://github.com/rrbanda/ai-agent-formatter)
- **Built With** → **FastAPI**, **Requests**, **PyYAML**, **CrewAI**

---
