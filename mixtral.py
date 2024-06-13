from langchain_community.llms import VLLMOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

mixtral_api_key = os.getenv("MIXTRAL_API_KEY")
mixtral_api_base = os.getenv("MIXTRAL_API_BASE")

llm = VLLMOpenAI(
    openai_api_key=mixtral_api_key,
    openai_api_base=mixtral_api_base,
    model_name="mistralai/Mixtral-8X7B-Instruct-v0.1",
    temperature=0.0,
    max_tokens=7000,
)

from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

messages = [
    {"role": "user", "content": "What is your favourite condiment?"},
    {
        "role": "assistant",
        "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!",
    },
    {"role": "user", "content": "Do you have mayonnaise recipes?"},
]

inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")

outputs = model.generate(inputs, max_new_tokens=20)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
