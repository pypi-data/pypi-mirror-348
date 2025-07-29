# https://huggingface.co/docs/transformers/v4.49.0/en/model_doc/auto#auto-classes
from transformers import AutoModelForCausalLM, AutoTokenizer

AI_ANSWERS_LENGTH = 300

models = [
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "Qwen/Qwen2.5-3B-Instruct",
]

for idx, model_name in enumerate(models):
    print(f"{idx}. {model_name}")
model_idx = int(input("Type model number and press Enter: "))

model = AutoModelForCausalLM.from_pretrained(models[model_idx])
tokenizer = AutoTokenizer.from_pretrained(models[model_idx])

try:
    while True:
        inputs = tokenizer(input("\nYour question >>> "), return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=AI_ANSWERS_LENGTH)
        print(f"\nA.I. answer >>> {tokenizer.decode(*outputs)}")
except KeyboardInterrupt:
    print("\nExit.")
