from config import (IDS_FILE, MAX_JOBS, OUTPUT_DIR, SEARCH_TERM, WAIT_INITIAL,
                    WAIT_SCROLL)
from gpt.gpt_decision import filter_and_classify_job
from gpt.gpt_mvp import generate_mvp_plan
from gpt.gpt_proposal import generate_proposal
from scraper import get_chrome_driver, scrape_jobs_with_pagination
from utils import (ensure_dir, extract_job_id, load_ids, save_ids,
                   save_job_summary)


def main():
    ensure_dir(OUTPUT_DIR)
    analyzed_ids = load_ids(IDS_FILE)
    driver = get_chrome_driver()
    url = f"https://www.upwork.com/nx/jobs/search/?q={SEARCH_TERM}"
    print(f"[LOG] Abrindo URL: {url}")
    driver.get(url)

    jobs = scrape_jobs_with_pagination(driver, analyzed_ids, MAX_JOBS, WAIT_INITIAL, WAIT_SCROLL)
    driver.quit()
    jobs = [job for job in jobs if "Fixed price" in job["job_type"]]

    print(f"[LOG] Encontrados {len(jobs)} jobs fixed price (mais novos primeiro).")
    novos = 0
    para_gpt = 0

    for job in jobs:
        job_id = extract_job_id(job)
        if not job_id:
            continue
        para_gpt += 1
        result = filter_and_classify_job(job)
        categoria = None
        panorama = ""
        if "aprovado: mvp" in result:
            categoria = "mvp"
            panorama = generate_mvp_plan(job)
        elif "aprovado: proposta" in result:
            categoria = "proposta"
            panorama = generate_proposal(job)
        else:
            print(f"[IGNORADO] {job['title']} ({job_id}) Não vale a pena ou falta info.")
            analyzed_ids.add(job_id)
            continue

        save_job_summary(job, panorama, OUTPUT_DIR, categoria)
        print(f"[APROVADO] {job['title']} ({job_id}) [{categoria}]")
        analyzed_ids.add(job_id)
        novos += 1

    save_ids(analyzed_ids, IDS_FILE)
    print(f"[OK] {para_gpt} jobs analisados, {novos} aprovados, resumos salvos em '{OUTPUT_DIR}/'.")

if __name__ == "__main__":
    main()
