import streamlit as st
import pandas as pd

# ---------------------------------
# Page Setup
# ---------------------------------
st.set_page_config(page_title="Real Job Search System", layout="wide")
st.title("🇮🇳 Real Job Search System")
st.write(
    "Browse real jobs using **normalized job roles**, location, and category. "
    "Internships are shown separately for freshers."
)

# ---------------------------------
# Load Jobs
# ---------------------------------
jobs_df = pd.read_csv("all_real_jobs.csv")
jobs_df = jobs_df.fillna("")

# ---------------------------------
# STRICT INTERNSHIP DETECTION (TITLE ONLY)
# ---------------------------------
def is_internship(title):
    title = title.lower()
    return any(k in title for k in ["intern", "internship", "trainee"])

jobs_df["is_internship"] = jobs_df["job_title"].apply(is_internship)

# ---------------------------------
# ROLE NORMALIZATION (KEY FIX)
# ---------------------------------
ROLE_MAP = {
    "Data Science": [
        "data scientist", "machine learning", "ml engineer", "ai", "applied scientist"
    ],
    "Software Engineer": [
        "software engineer", "sde", "developer", "programmer"
    ],
    "Backend": [
        "backend", "api", "microservice"
    ],
    "Frontend": [
        "frontend", "ui", "react", "angular"
    ],
    "DevOps": [
        "devops", "cloud", "aws", "docker", "kubernetes"
    ],
    "Data Analyst": [
        "data analyst", "analytics", "sql", "business analyst"
    ],
    "QA / Testing": [
        "qa", "test", "quality assurance"
    ],
    "Internship": [
        "intern", "internship", "trainee"
    ]
}

def normalize_role(title):
    title = title.lower()
    for role, keywords in ROLE_MAP.items():
        for k in keywords:
            if k in title:
                return role
    return "Other"

jobs_df["normalized_role"] = jobs_df["job_title"].apply(normalize_role)

# ---------------------------------
# SEARCH TEXT (FREE SEARCH)
# ---------------------------------
jobs_df["search_text"] = (
    jobs_df["job_title"] + " "
    + jobs_df["company"] + " "
    + jobs_df["location"] + " "
    + jobs_df["normalized_role"]
).str.lower()

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------
st.sidebar.header("Filters")

# Category
view = st.sidebar.radio(
    "Category",
    ["All Jobs", "Internships (Freshers)", "Experienced Jobs"]
)

# NORMALIZED JOB ROLE FILTER (FIXED)
roles = sorted(jobs_df["normalized_role"].unique())
selected_role = st.sidebar.selectbox(
    "Job Role",
    ["All"] + roles
)

# Location
locations = sorted(jobs_df["location"].unique())
selected_location = st.sidebar.selectbox(
    "Location",
    ["All"] + locations
)

# Search box
query = st.text_input(
    "🔍 Search (role / company / location)"
).lower()

# ---------------------------------
# FILTERING LOGIC
# ---------------------------------
filtered_df = jobs_df.copy()

# Category filter
if view == "Internships (Freshers)":
    st.info(
        "Showing only roles that explicitly mention **intern / internship / trainee** "
        "in the job title."
    )
    filtered_df = filtered_df[filtered_df["is_internship"] == True]

elif view == "Experienced Jobs":
    filtered_df = filtered_df[filtered_df["is_internship"] == False]

# Normalized role filter
if selected_role != "All":
    filtered_df = filtered_df[
        filtered_df["normalized_role"] == selected_role
    ]

# Location filter
if selected_location != "All":
    filtered_df = filtered_df[
        filtered_df["location"] == selected_location
    ]

# Search filter
if query:
    filtered_df = filtered_df[
        filtered_df["search_text"].str.contains(query, na=False)
    ]

# ---------------------------------
# DISPLAY JOB CARDS
# ---------------------------------
st.write(f"### Showing {len(filtered_df)} jobs")

if filtered_df.empty:
    st.warning("No jobs found.")
else:
    for _, row in filtered_df.iterrows():
        with st.container():
            st.markdown(
                f"""
                ### {row['job_title']}
                🏢 **{row['company']}**  
                📍 {row['location']}  
                🧭 Role: *{row['normalized_role']}*

                🔗 [Apply on Company Website]({row['link']})
                """
            )
            st.markdown("---")

# ---------------------------------
# FOOTER
# ---------------------------------
st.caption(
    "Jobs are grouped using normalized roles. "
    "Internships are shown only when explicitly stated in job titles."
)
