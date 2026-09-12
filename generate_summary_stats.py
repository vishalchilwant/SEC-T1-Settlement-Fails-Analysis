import os
import numpy as np
import pandas as pd

CSV_PATH = os.path.join("sec_ftd_data", "sec_ftd_clean_panel_2024.csv")

print("[*] Loading panel dataset from disk...")
df = pd.read_csv(
    CSV_PATH,
    parse_dates=["SETTLEMENT DATE"],
    dtype={"CUSIP": str, "SYMBOL": str},
)

# Calculate dollar volume if not present
if "DOLLAR_FTD" not in df.columns and "PRICE" in df.columns:
  df["DOLLAR_FTD"] = df["QUANTITY (FAILS)"] * df["PRICE"]

df["LOG_FTD"] = np.log(df["QUANTITY (FAILS)"] + 1)
df["POST_T1"] = (df["SETTLEMENT DATE"] >= pd.Timestamp("2024-05-28")).astype(
    int
)
df["PENNY_STOCK"] = (df["PRICE"] < 5.0).astype(int)

pre = df[df["POST_T1"] == 0]
post = df[df["POST_T1"] == 1]


def compute_metrics(sub_df, name):
  fails = sub_df["QUANTITY (FAILS)"]
  log_fails = sub_df["LOG_FTD"]
  dollars = sub_df["DOLLAR_FTD"].dropna()
  return {
      "Sample": name,
      "N": len(sub_df),
      "Unique CUSIPs": sub_df["CUSIP"].nunique(),
      "Mean FTD": fails.mean(),
      "Median FTD": fails.median(),
      "Std FTD": fails.std(),
      "Mean Log(FTD+1)": log_fails.mean(),
      "Std Log(FTD+1)": log_fails.std(),
      "Mean Dollar FTD ($)": dollars.mean(),
      "Median Dollar FTD ($)": dollars.median(),
  }


summary_rows = [
    compute_metrics(df, "Full Sample"),
    compute_metrics(pre, "Pre-Reform (T+2)"),
    compute_metrics(post, "Post-Reform (T+1)"),
    compute_metrics(df[df["PENNY_STOCK"] == 1], "Low-Price (< $5)"),
    compute_metrics(df[df["PENNY_STOCK"] == 0], "Standard (>= $5)"),
]

sum_table = pd.DataFrame(summary_rows)

print("\n" + "=" * 80)
print("                       EMPIRICAL SUMMARY STATISTICS")
print("=" * 80)
print(sum_table.to_string(index=False))
print("=" * 80)