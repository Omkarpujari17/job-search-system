import pandas as pd

greenhouse_df = pd.read_csv("greenhouse.csv")   # from Greenhouse
lever_df = pd.read_csv("lever.csv")        # from Lever

all_jobs = pd.concat([greenhouse_df, lever_df], ignore_index=True)

all_jobs.to_csv("all_real_jobs.csv", index=False)

print(f"✅ TOTAL JOBS AVAILABLE: {len(all_jobs)}")
print("✅ Saved to all_real_jobs.csv")
