# 🐆 **Leopard Pont des Arts - CrewAI Example**

This repository demonstrates the use of **CrewAI** to build an **AI agent** that computes the time it takes for a **leopard to cross the Pont des Arts bridge** in Paris. The agent leverages **LLM reasoning** and **external data sources** to compute the result.

Additionally, we've integrated a  **FastAPI service** , providing an API endpoint to access the agent programmatically.

---

## **🚀 Features**

✔️ **CrewAI-based intelligent agent**

✔️ **LLM-powered computation** (configurable)

✔️ **DuckDuckGo search for additional data**

✔️ **FastAPI for remote access via API**

✔️ **Config-driven approach** (YAML-based)

---

## **📂 Project Structure**

```
leopard_pontdesarts/
│── configs/               # 🔹 Configuration files
│   ├── config.yaml        # Global settings (LLM, API keys, etc.)
│   ├── agents.yaml        # Agent definition (role, backstory, etc.)
│   ├── prompts.yaml       # Prompt configurations
│   ├── tasks.yaml         # Task definitions
│
│── src/                   # 🔹 Source code
│   ├── main.py            # Entry point for execution
│   ├── agents.py          # CrewAI agent implementation
│   ├── tasks.py           # Task definitions
│   ├── llm.py             # LLM API integration
│   ├── api.py             # FastAPI service
│
│── venv/                  # 🔹 Python Virtual Environment
│── requirements.txt        # 🔹 Required dependencies
│── README.md               # 🔹 Project Documentation
```

---

## **🔧 Installation & Setup**

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/your-username/crewai-examples.git
cd crewai-examples/leopard_pontdesarts
```

### **2️⃣ Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4️⃣ Configure Your Settings**

Modify the `configs/config.yaml` file to set up your  **LLM API details** :

```yaml
llm:
  model: deepseek-r1-distill-qwen-14b
  api_url: "https://your-llm-api.com"
  api_key: "your-api-key"
```

---

## **🚀 Running the Agent**

To run the **Leopard Pont des Arts** agent, execute:

```bash
python -m src.main
```

🔹 This will trigger the CrewAI agent to compute the **leopard crossing time** using an LLM.

---

## **🌍 Running the API Server**

The project includes a **FastAPI** service to expose the agent as an API. Start the API server with:

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

Once running, access the API via:

* **Home Route:** [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/)
* **Leopard Crossing API:** [`http://127.0.0.1:8000/leopard-crossing`](http://127.0.0.1:8000/leopard-crossing)

📌 **Example API Call:**

```bash
curl http://127.0.0.1:8000/leopard-crossing
```

---

## **🛠 Configuration Files**

### **🔹 `configs/agents.yaml` (Agent Configuration)**

```yaml
leopard_pont_des_arts_agent:
  role: LeopardPontDesArtsAgent
  goal: Compute crossing time in seconds.
  backstory: >
    No chain-of-thought; single pass approach.
    Your job is to calculate how long it takes for a leopard to cross the Pont des Arts bridge.
```

### **🔹 `configs/prompts.yaml` (LLM Prompt)**

```yaml
leopard_pont_des_arts_prompt: |
  Given:
  - **Leopard's Speed**: 58 km/h
  - **Pont des Arts Bridge Length**: 155 meters

  ### Task:
  Compute the time in **seconds** for a leopard running at full speed to cross the Pont des Arts bridge.

  Use the formula:
  Time (seconds) = Distance (meters) / Speed (m/s)

  Return response in **JSON format**:

  ```json
  {
      "time_seconds": <numeric_value>,
      "explanation": "<brief explanation>"
  }
```

```

### **🔹 `configs/tasks.yaml` (Task Definition)**
```yaml
leopard_task:
  description: "How many seconds would it take for a leopard at full speed to run through Pont des Arts?"
  expected_output: "Approximate time in seconds + brief reasoning"
```

---

## **📌 Example Response**

When executed, the agent returns:

```json
{
  "time_seconds": 9.62,
  "explanation": "The leopard's speed is converted from km/h to m/s (58 km/h ≈ 16.111 m/s). Time is calculated by dividing the bridge length (155 meters) by the speed, resulting in approximately 9.62 seconds."
}
```

---

## **🛠 Troubleshooting**

* If  **FastAPI is not installed** , run:
  ```bash
  pip install fastapi uvicorn
  ```
* If  **LLM API is unreachable** , check your `config.yaml` for the correct **API URL** and  **API key** .
* To debug, enable verbose logging in `src/main.py`:
  ```python
  logging.basicConfig(level=logging.DEBUG)
  ```

---

## **📜 License**

This project is licensed under the  **MIT License** .

---

## **📬 Contact**

For questions or suggestions, feel free to reach out or open an issue in the repo.

---
