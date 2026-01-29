import streamlit as st
import pandas as pd

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Real Job Search System",
    page_icon="💼",
    layout="wide"
)

# -------------------------------------------------
# Load data
# -------------------------------------------------
@st.cache_data
def load_jobs():
    df = pd.read_csv("all_jobs.csv")
    df = df.fillna("")
    return df

jobs_df = load_jobs()

# -------------------------------------------------
# Internship detection (STRICT – title only)
# -------------------------------------------------
def is_internship(title):
    title = title.lower()
    return any(k in title for k in ["intern", "internship", "trainee"])

jobs_df["is_internship"] = jobs_df["job_title"].apply(is_internship)

# -------------------------------------------------
# Role normalization
# -------------------------------------------------
ROLE_MAP = {
    "Software Engineer": ["software engineer", "sde", "developer", "programmer"],
    "Backend Engineer": ["backend", "api", "microservice"],
    "Frontend Engineer": ["frontend", "react", "angular", "ui"],
    "Data Scientist": ["data scientist", "machine learning", "ml", "ai"],
    "Data Analyst": ["data analyst", "analytics", "sql"],
    "DevOps / Cloud": ["devops", "aws", "cloud", "docker", "kubernetes"],
    "QA / Testing": ["qa", "test", "quality"],
    "Internship": ["intern", "internship", "trainee"]
}

def normalize_role(title):
    t = title.lower()
    for role, keys in ROLE_MAP.items():
        if any(k in t for k in keys):
            return role
    return "Other"

jobs_df["normalized_role"] = jobs_df["job_title"].apply(normalize_role)

# -------------------------------------------------
# Search text
# -------------------------------------------------
jobs_df["search_text"] = (
    jobs_df["job_title"] + " "
    + jobs_df["company"] + " "
    + jobs_df["location"] + " "
    + jobs_df["normalized_role"]
).str.lower()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("## 💼 Real Job Search System")
st.caption(
    "Live jobs fetched daily from company career pages (Greenhouse & Lever). "
    "Click a job to apply on the official website."
)

# -------------------------------------------------
# Tabs
# -------------------------------------------------
tab_all, tab_intern = st.tabs(["All Jobs", "Internships"])

# -------------------------------------------------
# Sidebar filters
# -------------------------------------------------
st.sidebar.header("🔍 Filters")

role_filter = st.sidebar.selectbox(
    "Job Role",
    ["All"] + sorted(jobs_df["normalized_role"].unique())
)

location_filter = st.sidebar.selectbox(
    "Location",
    ["All"] + sorted(jobs_df["location"].unique())
)

search_query = st.sidebar.text_input(
    "Search (role / company / location)"
).lower()

# -------------------------------------------------
# Filtering function
# -------------------------------------------------
def apply_filters(df):
    if role_filter != "All":
        df = df[df["normalized_role"] == role_filter]

    if location_filter != "All":
        df = df[df["location"] == location_filter]

    if search_query:
        df = df[df["search_text"].str.contains(search_query, na=False)]

    return df

# -------------------------------------------------
# Job card renderer
# -------------------------------------------------
def render_job_cards(df):
    if df.empty:
        st.warning("No jobs found.")
        return

    for _, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([5, 1])

            with col1:
                st.markdown(
                    f"""
                    ### {row['job_title']}
                    **{row['company']}**  
                    📍 {row['location']}  
                    🧭 {row['normalized_role']}  
                    🏷 Source: {row.get("source", "ATS").title()}
                    """
                )

            with col2:
                st.markdown(
                    f"""
                    <a href="{row['link']}" target="_blank">
                        <button style="
                            background-color:#2563EB;
                            color:white;
                            padding:10px 16px;
                            border:none;
                            border-radius:6px;
                            cursor:pointer;
                        ">
                        Apply
                        </button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("---")

# -------------------------------------------------
# All Jobs tab
# -------------------------------------------------
with tab_all:
    filtered = apply_filters(jobs_df)
    st.subheader(f"📄 Showing {len(filtered)} jobs")
    render_job_cards(filtered)

# -------------------------------------------------
# Internship tab
# -------------------------------------------------
with tab_intern:
    st.info(
        "Showing only roles that explicitly mention **Intern / Internship / Trainee** "
        "in the job title."
    )
    intern_df = jobs_df[jobs_df["is_internship"] == True]
    intern_df = apply_filters(intern_df)
    st.subheader(f"🎓 Showing {len(intern_df)} internships")
    render_job_cards(intern_df)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption(
    "⚠️ This platform is a job discovery tool. "
    "All applications redirect to official company career pages."
)
