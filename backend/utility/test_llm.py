from llama_cpp import Llama

llm = Llama(
    model_path="models/Phi-3-mini-4k-instruct-q4.gguf",
    n_ctx=2048,
    n_threads=6,
)

out = llm("Explain Amla in Ayurveda in 5 lines.\n\n", max_tokens=200)
print(out["choices"][0]["text"])
