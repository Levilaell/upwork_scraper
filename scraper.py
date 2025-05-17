import time

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import extract_job_id


def get_chrome_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = uc.Chrome(options=options)
    return driver

def scrape_jobs_with_pagination(driver, analyzed_ids, max_jobs=None, wait_initial=6, wait_scroll=2):
    all_jobs = []
    page = 1

    while True:
        print(f"[LOG] Coletando jobs da página {page}...")
        time.sleep(wait_initial if page == 1 else wait_scroll)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        jobs = soup.select("article[data-test='JobTile']")
        print(f"[LOG] {len(jobs)} jobs encontrados nesta página.")

        for job in jobs:
            a_tag = job.select_one("a[data-test='job-tile-title-link UpLink']")
            title = a_tag.get_text(strip=True) if a_tag else ""
            link = "https://www.upwork.com" + a_tag['href'] if a_tag else ""
            posted = job.select_one("small[data-test='job-pubilshed-date']")
            posted_text = posted.get_text(strip=True).replace("Posted", "").strip() if posted else ""
            job_type = job.select_one("li[data-test='job-type-label']")
            job_type_text = job_type.get_text(strip=True) if job_type else ""
            exp_level = job.select_one("li[data-test='experience-level']")
            exp_level_text = exp_level.get_text(strip=True) if exp_level else ""
            budget = job.select_one("li[data-test='is-fixed-price']")
            budget_text = budget.get_text(strip=True) if budget else ""
            desc_div = job.select_one("div[data-test='UpCLineClamp JobDescription'] p")
            desc = desc_div.get_text(strip=True) if desc_div else ""
            tags = [tag.get_text(strip=True) for tag in job.select("button[data-test='token']")]
            job_dict = {
                "title": title,
                "link": link,
                "posted": posted_text,
                "job_type": job_type_text,
                "experience": exp_level_text,
                "budget": budget_text,
                "description": desc,
                "tags": ", ".join(tags),
            }
            job_id = extract_job_id(job_dict)
            if not job_id:
                continue
            if job_id in analyzed_ids:
                print(f"[LOG] Job já analisado ({job_id}), parando busca aqui.")
                return all_jobs
            all_jobs.append(job_dict)
            if max_jobs and len(all_jobs) >= max_jobs:
                return all_jobs

        # Próxima página
        try:
            next_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="next-page"]:not(:disabled)'))
            )
            next_btn.click()
            page += 1
        except Exception:
            print("[LOG] Não há mais páginas ou botão desabilitado.")
            break

    return all_jobs
