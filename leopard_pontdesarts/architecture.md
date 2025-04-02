graph TD

subgraph CrewAI_Agent_Workflow["🧠 CrewAI Agent Workflow"]
    A1["📄 Task YAML: leopard_pont_des_arts_task"] --> A2["🧠 Agent YAML: LeopardPontDesArtsAgent"]
    A2 --> A3["🛠️ Python Task Object (get_leopard_task)"]
    A3 --> A4["🤖 Crew(agents, tasks)"]
    A4 --> A5["🚀 crew.kickoff()"]
    A5 --> A6["🧠 LLM Inference via CustomLLM.infer"]
end

subgraph LLM_Config_Resolution["🔧 LLM Config Resolution"]
    B1["🔐 ENV (.env / ConfigMap)"]
    B2["📄 llm_provider_config.yaml"]
    B1 --> B4["🧩 CustomLLM init()"]
    B2 --> B4
    B4 --> A6
end

subgraph FastAPI_Layer["🌐 FastAPI API Layer"]
    C1["GET /leopard-crossing"] --> C2["⚙️ execute_leopard_task()"]
    C2 --> A5
    C3["GET /leopard-crossing-ui"] --> C2
    C3 --> D1["🎨 call_formatter()"]
end

subgraph Formatter_API["🎨 Formatter Integration"]
    D1 --> D2["POST /process to Formatter API"]
end

subgraph LLM_Provider["📊 LLM Backends"]
    A6 --> E1["VLLM / OpenAI-compatible"]
    A6 --> E2["Deepseek / Ollama"]
end
