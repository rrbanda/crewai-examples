# crewai-examples

# **LeopardPontDesArtsAgent Example**

This example demonstrates a **CrewAI-based** pipeline that:

1. Uses **DuckDuckGo** to gather facts about leopard top speeds and the length of Pont des Arts.  
2. Calls **local Ollama** running **Mistral** (via simple HTTP) to **estimate** how many seconds a leopard at full speed would take to cross Pont des Arts.  

## **Features**

- The agent **manually** calls DuckDuckGo and your local Ollama server.  
- **Single-Pass Approach**: No repeated “Thought: / Action:” format or advanced parsing.  
- **Local Mistral**: The `DirectOllama` class makes a straightforward `POST` request to `http://localhost:11434/api/generate`.  
- **CrewAI** orchestrates** the **agent** and **task** but does **not** impose chain-of-thought instructions.

---

## **Requirements**

1. **Python 3.8+** (with `pip` available).  
2. **Virtual Environment** recommended:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install --upgrade crewai langchain langchain_community duckduckgo-search requests
   ```
4. **Local Ollama** with **Mistral**:
   - Install [Ollama](https://github.com/jmorganca/ollama).  
   - Pull/run the Mistral model:
     ```bash
     ollama run mistral
     ```
     By default, it listens on `http://localhost:11434`.

---

## **How to Run**

1. **Start Ollama** with Mistral in **one** terminal:
   ```bash
   ollama run mistral
   ```
2. **Run** the script in **another** terminal:
   ```bash
   python crewai_leopard_pontdesarts.py
   ```
3. **Watch** the console:
   - The agent queries DuckDuckGo for relevant facts (bridge length, leopard top speed).  
   - The local **Mistral** model returns an **approximate time** in seconds, plus reasoning.

---

## **Code Walkthrough**

1. **DirectOllama**  
   - A minimal class that does **one** job: makes a `POST` request to `http://localhost:11434/api/generate` with your prompt.  
   - Returns the **final** text after reading the NDJSON stream.

2. **LeopardPontDesArtsAgent**  
   - Declares a **private** `_ddg` for DuckDuckGo queries.  
   - Declares a **private** `_ollama` for local Mistral calls.  
   - **`execute_task`**:
     1. Collects real-time data from DuckDuckGo.  
     2. Builds a single **prompt** with that data.  
     3. Sends the prompt to Mistral for final reasoning.  
     4. Returns the final textual answer.

3. **Task + Crew**  
   - Creates a **single** `Task` describing the question (“How many seconds…?”).  
   - **Crew** runs that task with our **agent** in a single pass.  

---

## **Notes**

- **No chain-of-thought** or LiteLLM usage. CrewAI **does** internally rely on some logic to unify LLM calls, but we bypass it by **not** registering an `llm` field.  
- The **search result** or final “Pont des Arts crossing time” is **approximate**—the script is purely for demonstration.  
- If you see **“LLM Provider NOT provided”** or **“LiteLLM call failed”** in logs, confirm you’re not storing an `llm` field on the agent. Instead, we do everything manually in `execute_task`.

---

## **Potential Extensions**

- **Multi-Agent**: If you want more complex workflows, define multiple tasks or agents.  
- **Refined Summaries**: Adjust the Mistral prompt for bullet points, multi-paragraph answers, etc.  
- **Additional Tools**: Beyond DuckDuckGo, you can integrate other `langchain_community` utilities.

---

## **License & Credits**

- **CrewAI** code is credited to [CrewAI on GitHub](https://github.com/Cognitive-Initiative/crewai).  
- **Mistral** model courtesy of the Mistral creators.  
- **DuckDuckGoSearchAPIWrapper** from [LangChain Community](https://github.com/hwchase17/langchain).  

Feel free to modify and redistribute this example as you see fit. Enjoy building with **CrewAI + Ollama**!
