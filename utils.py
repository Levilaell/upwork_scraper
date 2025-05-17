import os
import re


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_ids(path):
    if not os.path.exists(path):
        return set()
    with open(path, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_ids(ids, path):
    with open(path, "w") as f:
        for job_id in sorted(ids):
            f.write(job_id + "\n")

def extract_job_id(job):
    # Extrai o ID do job a partir do link ou do dicionário
    link = job.get("link", "")
    match = re.search(r'~0?(\d+)', link)
    if match:
        return match.group(1)
    # Tenta pelo final do link se não for o formato padrão
    return link.split("~")[-1].split("/")[0] if "~" in link else None

def save_job_summary(job, panorama, output_dir, categoria):
    file_name = f"{categoria}_{extract_job_id(job)}.txt"
    path = os.path.join(output_dir, file_name)
    with open(path, "w") as f:
        f.write(f"Título: {job['title']}\n")
        f.write(f"Link: {job['link']}\n")
        f.write(f"Orçamento: {job['budget']}\n")
        f.write(f"Descrição: {job['description']}\n")
        f.write(f"Tags: {job['tags']}\n")
        f.write(f"\nPanorama:\n{panorama}\n")
