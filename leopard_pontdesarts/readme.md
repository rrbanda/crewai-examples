# **🚀 LeopardPontDesArts CrewAI Project - README**

> **Compute how long a leopard would take to cross the Pont des Arts bridge using AI! 🐆🌉**

---

## **📌 Project Overview**

This project uses **CrewAI** to create an AI-powered agent that:

1. **Searches the web** for information on leopard speeds using  **DuckDuckGo** .
2. **Calculates the time** it would take for a leopard running at full speed to cross the  **Pont des Arts bridge** .
3. **Interacts with a Language Model (LLM)** to generate a structured JSON response.
4. **Formats the output properly** for easy interpretation.

---

## **📁 Project Structure**

```bash
leopard_pontdesarts/
│── src/
│   ├── agents.py      # Defines AI agents (LeopardPontDesArtsAgent)
│   ├── tasks.py       # Defines the specific tasks the agents will perform
│   ├── llm.py         # Handles LLM API calls and JSON extraction
│   ├── main.py        # Main entry point to execute the AI pipeline
│   ├── __init__.py    # Allows src to be recognized as a module
│── requirements.txt   # Lists required Python dependencies
│── .env.example       # Example of environment variables needed
│── README.md          # This file! 📖
```

---

## **🛠️ Setup Instructions**

### **1️⃣ Install Dependencies**

Make sure you have Python **3.10+** installed.

```bash
# Clone the repository
git clone https://github.com/your-repo/leopard_pontdesarts.git
cd leopard_pontdesarts

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install required dependencies
pip install -r requirements.txt
```

### **2️⃣ Configure Environment Variables**

Create a `.env` file in the **project root directory** and add the following details:

```ini
LLM_API_URL="https://your-llm-api-url.com"
LLM_MODEL="your-llm-model-name"
LLM_API_KEY="your-secret-api-key"
```

Replace `"your-llm-api-url.com"`, `"your-llm-model-name"`, and `"your-secret-api-key"` with your actual API details.

---

## **🚀 Running the AI Agent**

Navigate to the project directory and run:

```bash
python -m src.main
```

**Expected Output:**

```json
{
  "time_seconds": 9.62,
  "explanation": "The leopard's speed is converted to meters per second (16.111 m/s), and the bridge length (155 meters) is divided by this speed to get the time in seconds."
}
```

---

## **🧐 How It Works**

### **1️⃣ Agents (src/agents.py)**

* **LeopardPontDesArtsAgent** is responsible for answering:
  * *"How many seconds would it take for a leopard to cross the Pont des Arts bridge?"*
* It fetches relevant data using **DuckDuckGo search** and interacts with an **LLM API** to generate a structured response.

### **2️⃣ Tasks (src/tasks.py)**

* Defines a **specific task** for the agent:
  * **Computing the crossing time**
  * Expecting an output format: `{"time_seconds": X.XX, "explanation": "..."}`

### **3️⃣ LLM API Handler (src/llm.py)**

* Calls the **LLM API** with a prompt.
* **Extracts JSON** response from the AI-generated text.
* **Retries** in case of failures.

### **4️⃣ CrewAI Execution (src/main.py)**

* **Defines the Crew (AI Workflow)**
* Executes the defined **task**
* Prints the  **final result in JSON format** .

---

## **🔧 Troubleshooting**

### ❌ **ModuleNotFoundError: No module named 'src'**

Run the script with `-m`:

```bash
python -m src.main
```

or ensure you're in the **correct directory** before running.

### ❌ **ImportError: pydantic_core not found**

Try reinstalling dependencies:

```bash
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ **LLM API not responding**

* Ensure **LLM_API_URL** is correct in `.env`.
* Check if the **API Key** is valid.

---

## **🎯 Next Steps**

✅ **Customize the Task** – Modify `src/tasks.py` to test different speed/distance scenarios.

✅ **Expand with New Agents** – Add another agent to compute results for  **cheetahs or humans** .

✅ **Deploy on OpenShift AI** – Make it production-ready!

---

## **📌 Summary**

This project provides an AI-powered **scientific calculator** 🧠 that:

* **Searches online** for relevant data 🔍
* **Interacts with an LLM API** for reasoning 🤖
* **Outputs structured results** in JSON format 📝

🎯 **🚀 Have fun experimenting and improving this AI workflow!** 🚀
