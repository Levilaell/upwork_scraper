import requests

from config import GPT_MAX_TOKENS, GPT_MODEL, GPT_TEMPERATURE, OPENAI_API_KEY

MVP_PROMPT = """
Você é um engenheiro de software freelancer. Resuma em até 6 linhas:

* Requisitos essenciais do job
* O que entregar no MVP funcional
* Mini plano de ação para implementar e demonstrar para o cliente.

Título: {title}
Descrição: {description}
Tipo: {job_type}
Nível de experiência: {experience}
Orçamento: {budget}
Tags: {tags}

Responda em português, de forma bem prática.
"""

def generate_mvp_plan(job):
    prompt = MVP_PROMPT.format(**job)
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GPT_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": GPT_MAX_TOKENS,
        "temperature": GPT_TEMPERATURE,
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print("[ERRO GPT]", response.status_code, response.text)
        return "Erro ao gerar plano MVP."
