# SEC T+1 Settlement Fails Analysis

Replication package for the empirical research paper: *"Compressing the Settlement Cycle: Cross-Sectional Frictions and Settlement Fails Under the SEC's T+1 Mandate"*.

## Overview
This repository contains the Python data pipeline used to process raw SEC Continuous Net Settlement (CNS) Fails-to-Deliver files and generate the empirical summary statistics and regression inputs surrounding the May 28, 2024, $T+1$ regulatory transition.

## Repository Structure
```text
├── sec_ftd_data/                # Directory for raw ZIP files and processed panel CSV
├── ingest_sec_ftd.py            # Processes raw SEC CNS zips into a clean panel dataset
├── generate_summary_stats.py    # Computes descriptive statistics (Table 1 outputs)
└── README.md                    # Project documentation
