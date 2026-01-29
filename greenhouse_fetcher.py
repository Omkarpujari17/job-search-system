import requests
import pandas as pd

# -------------------------------------------------
# Greenhouse companies (large, known list)
# -------------------------------------------------
GREENHOUSE_COMPANIES = [
    # Indian & India-hiring companies
    "swiggy", "zomato", "meesho", "groww", "phonepe", "cred",
    "razorpay", "inmobi", "sharechat", "udaan", "nykaa",
    "unacademy", "browserstack", "chargebee", "postman",
    "mindtickle", "lenskart", "dream11", "navi", "olacabs",
    "rapido", "zepto", "dunzo", "urbancompany",

    # Global product / SaaS companies (hire in India)
    "stripe", "airbnb", "coinbase", "snowflake", "databricks",
    "atlassian", "hubspot", "gitlab", "twilio", "zendesk",
    "elastic", "spotify", "dropbox", "okta", "asana",
    "notion", "figma", "slack", "confluent",

    # Enterprise & tech companies
    "freshworks", "zoho", "intuit", "servicenow",
    "salesforce", "vmware", "nutanix", "paloaltonetworks",
    "mongodb", "cloudera", "hashicorp", "splunk",

    # Fintech / startups
    "zerodha", "coin-switch", "slice", "bharatpe",
    "credavenue", "fi", "onecard"
]

# -------------------------------------------------
# Fetch jobs from a single Greenhouse company
# -------------------------------------------------
def fetch_greenhouse_jobs(company_slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
    except Exception:
        return []

    jobs = []

    for job in data.get("jobs", []):
        jobs.append({
            "job_title": job.get("title", ""),
            "company": company_slug.replace("-", " ").title(),
            "location": job.get("location", {}).get("name", ""),
            "link": job.get("absolute_url", ""),
            "description": job.get("content", "")
        })

    return jobs


# -------------------------------------------------
# Main runner
# -------------------------------------------------
if __name__ == "__main__":
    all_jobs = []

    print("🔄 Fetching jobs from Greenhouse companies...\n")

    for company in GREENHOUSE_COMPANIES:
        print(f"Fetching jobs from {company}...")
        try:
            jobs = fetch_greenhouse_jobs(company)
            print(f"  → {len(jobs)} jobs found")
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"  ❌ Failed for {company}: {e}")

    df = pd.DataFrame(all_jobs)
    df.to_csv("greenhouse.csv", index=False)

    print("\n✅ DONE")
    print(f"✅ TOTAL JOBS FETCHED: {len(df)}")
    print("✅ Saved to greenhouse.csv")
