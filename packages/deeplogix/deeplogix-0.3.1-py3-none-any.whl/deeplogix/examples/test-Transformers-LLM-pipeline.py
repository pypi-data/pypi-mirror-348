# https://huggingface.co/docs/transformers/v4.49.0/en/pipeline_tutorial#pipelines-for-inference
from transformers import pipeline

AI_ANSWERS_LENGTH = 300

models = [
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "Qwen/Qwen2.5-3B-Instruct",
]

for idx, model_name in enumerate(models):
    print(f"{idx}. {model_name}")
model_idx = int(input("Type model number and press Enter: "))

pipe = pipeline("text-generation", model=models[model_idx])

try:
    while True:
        inputs = input("\nYour question >>> ")
        outputs = pipe(inputs, max_new_tokens=AI_ANSWERS_LENGTH, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        print(f"\nA.I. answer >>> {outputs[0]['generated_text']}")
except KeyboardInterrupt:
    print("\nExit.")
