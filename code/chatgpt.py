from openai import OpenAI
import json

with open(r"textfiles\config.txt", "r") as file:
    data = json.loads(file.read())

api_key = data["api_key"]
client = OpenAI(api_key=api_key)

def get_response_for_prompt(prompt:str)-> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[{"role": "user", "content": prompt}])

    return response.choices[0].message.content

def get_text_embedding(input:str):
    response = client.embeddings.create(
    input= input,
    model="text-embedding-3-small"
)
    return response.data[0].embedding


def myopenai(query):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=[{"role": "user", "content": query}]
    )
    return completion.choices[0].message.content