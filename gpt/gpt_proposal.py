import requests

from config import GPT_MAX_TOKENS, GPT_MODEL, GPT_TEMPERATURE, OPENAI_API_KEY

PROPOSAL_PROMPT = """
Você é um engenheiro de software freelancer na Upwork. Escreva uma proposta objetiva, sucinta (4-6 linhas), mencionando rapidamente os requisitos principais e sugerindo abordagem inicial para este job:

Título: {title}
Descrição: {description}
Tipo: {job_type}
Nível de experiência: {experience}
Orçamento: {budget}
Tags: {tags}

Responda em português.
"""

def generate_proposal(job):
    prompt = PROPOSAL_PROMPT.format(**job)
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
        return "Erro ao gerar proposta."
