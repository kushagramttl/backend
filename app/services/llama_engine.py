from llama_cpp import Llama
import os

MODEL_PATH = os.path.join("models", "llama-2-7b.Q4_0.gguf")

# Load the model once
llm = Llama(model_path=MODEL_PATH, n_ctx=4096, n_threads=4)

def generate_response(prompt: str) -> str:
    result = llm(prompt, max_tokens=1000, temperature=0.3, stop=["Q:"])
    return result["choices"][0]["text"].strip()
