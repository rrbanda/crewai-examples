# 🏃‍♂️ **Leopard Pont des Arts CrewAI Example**

## 📌 **Overview**

This project is a **CrewAI-based agent simulation** designed to calculate how long it takes for a **leopard running at full speed** to cross the **Pont des Arts bridge** in Paris. The agent dynamically retrieves and processes the required data using a **configured LLM** and a  **custom prompt** .

---

## 📁 **Project Structure**

```
leopard_pontdesarts/
│── configs/
│   ├── agents.yaml      # Configurations for CrewAI agent
│   ├── prompts.yaml     # Prompt configurations for LLM
│   ├── tasks.yaml       # Task descriptions & expected output
│   ├── config.yaml      # General configurations (LLM API details, etc.)
│── src/
│   ├── agents.py        # Defines the LeopardPontDesArtsAgent class
│   ├── llm.py           # Handles LLM API requests and responses
│   ├── tasks.py         # Task creation and assignment
│   ├── main.py          # Entry point for running the Crew
│   ├── utils.py         # Helper functions for config loading
│── venv/                # (Optional) Virtual environment
│── README.md            # 📌 You are here!
```

---

## 🚀 **How It Works**

1. The **CrewAI Agent** is initialized based on `configs/agents.yaml`.
2. It uses a **custom prompt** (from `configs/prompts.yaml`) to compute crossing time.
3. A request is sent to the **LLM API** (from `configs/config.yaml`).
4. The agent **processes the response** and returns a  **structured JSON result** .

---

## ⚙️ **Configuration Files**

All configs are stored under `configs/`.

### **📌 `configs/agents.yaml`**

```yaml
leopard_pont_des_arts_agent:
  role: LeopardPontDesArtsAgent
  goal: Compute crossing time in seconds.
  backstory: >
    No chain-of-thought; single pass approach. 
    Your job is to calculate how long it takes for a leopard to cross the Pont des Arts bridge.
```

### **📌 `configs/prompts.yaml`**

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

### **📌 `configs/tasks.yaml`**
```yaml
leopard_task:
  description: "How many seconds would it take for a leopard at full speed to run through Pont des Arts?"
  expected_output: "Approximate time in seconds + brief reasoning"
```

### **📌 `configs/config.yaml`**

```yaml
llm:
  model: "deepseek-r1-distill-qwen-14b"
  api_url: "https://your-llm-url.com"
  api_key: "your-api-key"
```

---

## 🛠 **Setup & Installation**

### 1️⃣ **Clone the repository**

```bash
git clone https://github.com/rrbanda/crewai-examples.git
cd crewai-examples/leopard_pontdesarts
```

### 2️⃣ **Create a Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # (On Windows, use `venv\Scripts\activate`)
```

### 3️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## 🚀 **Run the Crew**

```bash
python -m src.main
```

🔹 This will initialize the CrewAI system and execute the Leopard Pont des Arts task.

---

## 📌 **Example Output**

```json
{
  "time_seconds": 9.62,
  "explanation": "The leopard's speed is converted from km/h to m/s (58 km/h ≈ 16.111 m/s). Time is calculated by dividing the bridge length (155 meters) by the speed (16.111 m/s), resulting in approximately 9.62 seconds."
}
```

---

## 🛠 **Debugging & Common Issues**

### 🔴 **Config file not found**

* Ensure all **YAML files exist** in the `configs/` folder.
* Run:
  ```bash
  ls configs/
  ```

### 🔴 **LLM API errors**

* Check if the **LLM API URL is correct** in `configs/config.yaml`.
* Ensure your API key is **valid and has access** to the model.

---

## 🏗 **Future Enhancements**

* 🔹 **Dynamic agent creation** from YAML.
* 🔹  **Multiple LLM model support** .
* 🔹 **UI for visualization** of the leopard's run time.

---

## 🤝 **Contributing**

* Feel free to submit **pull requests** or report **issues** [here](https://github.com/rrbanda/crewai-examples/issues).

---

## 📜 **License**

MIT License. See `LICENSE` for details. 🚀
