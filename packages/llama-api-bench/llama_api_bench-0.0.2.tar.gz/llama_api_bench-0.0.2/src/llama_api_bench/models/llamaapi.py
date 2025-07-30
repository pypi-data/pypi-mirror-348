# Models and their unsupported test cases

LLAMA_API_MODELS: dict[str, list[str]] = {
    "Llama-4-Scout-17B-16E-Instruct-FP8": [],
    "Llama-4-Maverick-17B-128E-Instruct-FP8": [],
    "Llama-3.3-70B-Instruct": ["vision"],
    "Llama-3.3-8B-Instruct": ["vision"],
    "Cerebras-Llama-4-Scout-17B-16E-Instruct": ["vision"],
    "Cerebras-Llama-3.3-70B-Instruct": ["vision"],
    "Groq-Llama-4-Maverick-17B-128E-Instruct": ["vision"],
    "Groq-Llama-3.3-70B-Instruct": ["structured_output", "vision"],
}
