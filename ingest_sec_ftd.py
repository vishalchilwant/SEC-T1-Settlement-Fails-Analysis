import os
import zipfile
import numpy as np
import pandas as pd

OUTPUT_DIR = "sec_ftd_data"
ZIP_FILES = [
    "cnsfails202403a.zip", "cnsfails202403b.zip",
    "cnsfails202404a.zip", "cnsfails202404b.zip",
    "cnsfails202405a.zip", "cnsfails202405b.zip",
    "cnsfails202406a.zip", "cnsfails202406b.zip",
    "cnsfails202407a.zip", "cnsfails202407b.zip",
    "cnsfails202408a.zip", "cnsfails202408b.zip"
]

dataframes = []

for zf in ZIP_FILES:
    path = os.path.join(OUTPUT_DIR, zf)
    if not os.path.exists(path):
        continue
    
    with zipfile.ZipFile(path) as z:
        for inner in z.namelist():
            print(f"Reading {inner} from {zf}...", flush=True)
            try:
                df = pd.read_csv(
                    z.open(inner),
                    delimiter='|',
                    dtype={'CUSIP': str, 'SYMBOL': str, 'QUANTITY (FAILS)': str, 'PRICE': str},
                    on_bad_lines='skip',
                    encoding='latin1'
                )
                dataframes.append(df)
                print(f" -> Successfully loaded {len(df):,} records!")
            except Exception as e:
                print(f" -> Error reading {inner}: {e}")

if dataframes:
    print("\nAssembling full panel dataset...")
    full_df = pd.concat(dataframes, ignore_index=True)
    full_df.columns = full_df.columns.str.strip().str.upper()

    full_df['SETTLEMENT DATE'] = pd.to_datetime(full_df['SETTLEMENT DATE'].astype(str), format='%Y%m%d', errors='coerce')
    full_df = full_df.dropna(subset=['SETTLEMENT DATE', 'CUSIP'])
    full_df['PRICE'] = pd.to_numeric(full_df['PRICE'].astype(str).str.replace('$', '').str.strip(), errors='coerce')
    full_df['QUANTITY (FAILS)'] = pd.to_numeric(full_df['QUANTITY (FAILS)'], errors='coerce').fillna(0)
    full_df = full_df.sort_values(by=['CUSIP', 'SETTLEMENT DATE']).reset_index(drop=True)
    
    # Shock date May 28, 2024
    full_df['POST_T1'] = (full_df['SETTLEMENT DATE'] >= pd.Timestamp('2024-05-28')).astype(int)
    full_df['LOG_FTD'] = np.log(full_df['QUANTITY (FAILS)'] + 1)

    out_file = os.path.join(OUTPUT_DIR, "sec_ftd_clean_panel_2024.csv")
    full_df.to_csv(out_file, index=False)
    print(f"\n=======================================================")
    print(f"SUCCESS! Cleaned dataset saved to: {out_file}")
    print(f"Total Observations: {len(full_df):,}")
    print(f"Unique Securities: {full_df['CUSIP'].nunique():,}")
    print(f"=======================================================")