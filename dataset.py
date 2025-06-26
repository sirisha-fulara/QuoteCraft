import asyncio
from playwright.async_api import async_playwright
import csv

# Add all your high-demand gig categories here 👇
SEARCH_TERMS = [
    "data science", "python", "machine learning", "web scraping",
    "wordpress", "seo", "resume writing", "ui ux design",
    "video editing", "logo design", "email marketing", "virtual assistant", "digital marketing"
]
PAGES_TO_SCRAPE = 5  # Adjust based on need

async def scrape_freelancer():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        all_results = []

        for term in SEARCH_TERMS:
            print(f"\n🔍 Scraping category: {term}")
            base_url = f"https://www.freelancer.com/jobs/{term.replace(' ', '-')}/"

            for page_num in range(1, PAGES_TO_SCRAPE + 1):
                url = base_url + f"?page={page_num}"
                print(f"- Page {page_num}: {url}")
                try:
                    await page.goto(url, timeout=60000)
                    await page.wait_for_selector('div.JobSearchCard-item', timeout=10000)
                except Exception as e:
                    print(f"⚠️ Failed to load {url}: {e}")
                    continue

                job_cards = await page.query_selector_all('div.JobSearchCard-item')
                for job in job_cards:
                    title_el = await job.query_selector('a.JobSearchCard-primary-heading-link')
                    title = await title_el.inner_text() if title_el else "N/A"
                
                    budget_el = await job.query_selector('div.JobSearchCard-primary-price')
                    budget = await budget_el.inner_text() if budget_el else "N/A"

                    skills_el = await job.query_selector_all('a.JobSearchCard-primary-tags-link')
                    skills = ", ".join([await s.inner_text() for s in skills_el]) if skills_el else "N/A"

                    desc_el = await job.query_selector('p.JobSearchCard-primary-description')
                    description = await desc_el.inner_text() if desc_el else "N/A"

                    all_results.append({
                        "category": term,
                        "title": title.strip(),
                        "budget": budget.strip(),
                        "skills": skills.strip(),
                        "description": description.strip(),
                    })

        await browser.close()

        # Save to CSV
        keys = all_results[0].keys() if all_results else ["category", "title", "budget", "skills", "description", "posted"]
        with open("freelancer_raw.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_results)

        print(f"\n✅ Scraped {len(all_results)} gigs across {len(SEARCH_TERMS)} categories. Saved to freelancer_gigs_full.csv")

if __name__ == "__main__":
    asyncio.run(scrape_freelancer())
