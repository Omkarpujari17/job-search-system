import requests
import pandas as pd

# -------------------------------------------------
# Lever companies (large, known list)
# -------------------------------------------------
LEVER_COMPANIES = [
    # Indian & India-hiring companies
    "unacademy", "nykaa", "udaan", "zepto", "bharatpe",
    "slice", "urbancompany", "porter", "rapido", "olacabs",
    "meesho", "lenskart", "cultfit", "credavenue", "payu",
    "policybazaar", "spinny", "cars24", "delhivery",

    # Global product / SaaS companies
    "netflix", "uber", "airtable", "robinhood", "coinbase",
    "pinterest", "snap", "reddit", "tiktok", "discord",
    "zoom", "shopify", "canva", "atlassian", "datadog",
    "cloudflare", "palantir", "brex", "affirm",

    # Developer / SaaS platforms
    "hashnode", "replit", "algolia", "segment",
    "mixpanel", "newrelic", "sentry", "auth0",

    # AI / Data / Security companies
    "openai", "huggingface", "deepmind", "anthropic",
    "scaleai", "databricks", "snowflake", "elastic",

    # Fintech / startups
    "stripe", "wise", "revolut", "klarna", "plaid",
    "razorpay", "phonepe", "groww", "zerodha"
]

# -------------------------------------------------
# Fetch jobs from a single Lever company
# -------------------------------------------------
def fetch_lever_jobs(company_slug):
    url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
    except Exception:
        return []

    jobs = []

    for job in data:
        jobs.append({
            "job_title": job.get("text", ""),
            "company": company_slug.replace("-", " ").title(),
            "location": job.get("categories", {}).get("location", ""),
            "link": job.get("hostedUrl", ""),
            "description": job.get("descriptionPlain", "")
        })

    return jobs


# -------------------------------------------------
# Main runner
# -------------------------------------------------
if __name__ == "__main__":
    all_jobs = []

    print("🔄 Fetching jobs from Lever companies...\n")

    for company in LEVER_COMPANIES:
        print(f"Fetching jobs from {company}...")
        try:
            jobs = fetch_lever_jobs(company)
            print(f"  → {len(jobs)} jobs found")
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"  ❌ Failed for {company}: {e}")

    df = pd.DataFrame(all_jobs)
    df.to_csv("lever.csv", index=False)

    print("\n✅ DONE")
    print(f"✅ TOTAL JOBS FETCHED: {len(df)}")
    print("✅ Saved to lever.csv")
