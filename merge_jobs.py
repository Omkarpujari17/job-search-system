import pandas as pd

# -------------------------------
# Load datasets
# -------------------------------
greenhouse_df = pd.read_csv("greenhouse.csv")
lever_df = pd.read_csv("lever.csv")

# -------------------------------
# Add source column
# -------------------------------
greenhouse_df["source"] = "greenhouse"
lever_df["source"] = "lever"

# -------------------------------
# Normalize text columns
# -------------------------------
def normalize_text(text):
    if pd.isna(text):
        return ""
    return str(text).strip().lower()

for df in [greenhouse_df, lever_df]:
    df["job_title_norm"] = df["job_title"].apply(normalize_text)
    df["company_norm"] = df["company"].apply(normalize_text)
    df["location_norm"] = df["location"].apply(normalize_text)

# -------------------------------
# Merge datasets
# -------------------------------
merged_df = pd.concat([greenhouse_df, lever_df], ignore_index=True)

# -------------------------------
# Remove duplicates
# -------------------------------
merged_df = merged_df.drop_duplicates(
    subset=["job_title_norm", "company_norm", "location_norm"],
    keep="first"
)

# -------------------------------
# Drop helper columns
# -------------------------------
merged_df = merged_df.drop(
    columns=["job_title_norm", "company_norm", "location_norm"]
)

# -------------------------------
# Save final dataset
# -------------------------------
merged_df.to_csv("all_jobs.csv", index=False)

print("✅ MERGE COMPLETE")
print(f"📊 Total jobs after merge: {len(merged_df)}")
print("💾 Saved as all_jobs.csv")
