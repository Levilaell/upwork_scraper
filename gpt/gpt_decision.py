import requests

from config import GPT_MAX_TOKENS, GPT_MODEL, GPT_TEMPERATURE, OPENAI_API_KEY

FILTER_PROMPT = """
Você é um engenheiro de software freelancer avaliando jobs na Upwork. Para o job abaixo, responda apenas uma linha:

* Se está dentro de áreas como: script, automação, API's ou desenvolvimento web.
* Se vale a pena, é tranquilo de executar e já tem todas as informações para começar, responda: aprovado: mvp (se já permite entregar um MVP funcional) ou aprovado: proposta (se falta algum detalhe para o MVP, mas vale a pena e é tranquilo).
* Caso NÃO valha a pena, NÃO seja tranquilo, ou NÃO tenha informações suficientes, responda: ignorado.

Título: {title}
Descrição: {description}
Tipo: {job_type}
Nível de experiência: {experience}
Orçamento: {budget}
Tags: {tags}
"""

def filter_and_classify_job(job):
    prompt = FILTER_PROMPT.format(**job)
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GPT_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 12,   # só precisa de 1 linha
        "temperature": GPT_TEMPERATURE,
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip().lower()
    else:
        print("[ERRO GPT]", response.status_code, response.text)
        return "ignorado"
