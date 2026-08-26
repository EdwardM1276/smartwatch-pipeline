# Smartwatch Market Analytics Platform

A production-grade end-to-end data pipeline that ingests, validates, cleans, enriches, and visualizes smartwatch market data. Built with Python, Pandas, and Streamlit, the platform automates the entire ETL workflow and provides a live, interactive dashboard for real-time market intelligence.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Pipeline](#running-the-pipeline)
  - [Running the Dashboard](#running-the-dashboard)
- [Deployment](#deployment)
- [Dashboard Demo](#dashboard-demo)
- [Data Pipeline Details](#data-pipeline-details)
- [Future Work](#future-work)
- [License](#license)

---

## Overview

The platform processes raw smartwatch product data (450+ records across 18 brands) through a modular ETL pipeline, performing automated validation, cleaning, and feature engineering. The enriched dataset is then served through an interactive Streamlit dashboard, enabling stakeholders to explore pricing trends, rating distributions, and brand performance in real-time.

**Key Outcome:** Eliminated 2+ hours of manual data preparation per week through full automation.

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Data Source   │────▶│   ETL Pipeline  │────▶│  Data Warehouse │
│  (raw CSV)      │     │   (Python)      │     │  (CSV/JSON)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │                           │
                              ▼                           ▼
                      ┌─────────────────┐     ┌─────────────────┐
                      │  CI/CD Pipeline │     │   Streamlit     │
                      │  (GitHub Actions)│     │   Dashboard     │
                      └─────────────────┘     └─────────────────┘
```

---

## Features

### Data Engineering
- **Modular ETL framework** with separation of concerns (config, logging, validation, feature engineering)
- **Automated schema validation** with strict type enforcement
- **Intelligent missing-value handling**: median imputation for numeric fields, mode imputation for categorical fields
- **Outlier detection and removal** (price/rating range validation)
- **10+ derived features**: price tiers, discount categories, value-for-money scores, brand popularity indices, and more
- **Structured logging** with file rotation and severity levels
- **Automated reporting**: JSON and CSV outputs with pipeline metadata

### Analytics & Visualization
- **Interactive Streamlit dashboard** with dynamic multi-filter capabilities
- **Real-time visualizations**: price distribution by tier, rating scatter plots, brand dominance charts
- **Correlation analysis** to uncover market trends
- **Live deployment** accessible to stakeholders without technical expertise

### Automation & DevOps
- **CI/CD pipeline via GitHub Actions** with scheduled weekly execution (cron)
- **Manual trigger capability** (`workflow_dispatch`) for on-demand runs
- **Automated Git commits** of processed data and pipeline reports
- **Containerized execution** via Docker for reproducibility

---

## Tech Stack

### Core
- **Python 3.9+**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Matplotlib / Seaborn** - Data visualization

### Dashboard
- **Streamlit** - Interactive web application

### DevOps
- **GitHub Actions** - CI/CD and automation
- **Docker** - Containerization (optional)
- **Structured Logging** - Rotating log files

---

## Project Structure

```
smartwatch_analytics/
├── src/                           # Core ETL modules
│   ├── __init__.py
│   ├── config.py                  # Configuration and schema definitions
│   ├── logger.py                  # Structured logging setup
│   ├── data_validator.py          # Schema and quality checks
│   └── feature_engineer.py        # Feature generation and cleaning
├── data/                          # Data storage
│   ├── raw/                       # Raw input (not tracked)
│   ├── processed/                 # Cleaned/enriched output
│   ├── logs/                      # Pipeline logs
│   └── reports/                   # Pipeline reports (JSON)
├── dashboard.py                   # Streamlit application
├── pipeline.py                    # Main orchestration script
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container configuration
├── .github/                       # CI/CD workflows
│   └── workflows/
│       └── run_pipeline.yml       # Weekly automation
└── README.md                      # This file
```

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/smartwatch-analytics.git
cd smartwatch-analytics
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

### Running the Pipeline

1. **Place your raw data** in the project root as `smartwatches.csv`

2. **Execute the ETL pipeline**

```bash
python pipeline.py
```

3. **Check the output** in `data/processed/`:
   - `smartwatches_clean.csv` - Cleaned and enriched data
   - `smartwatches_clean.json` - JSON version for API consumption

4. **View pipeline reports** in `data/reports/`

### Running the Dashboard

After running the pipeline:

```bash
streamlit run dashboard.py
```

Navigate to `http://localhost:8501` in your browser.

---




```bash
docker build -t smartwatch-pipeline .
docker run smartwatch-pipeline
```

---

## Dashboard Demo

The live dashboard enables stakeholders to:

- **Filter** by brand and price tier
- **View** key metrics: total models, average price, average rating, unique brands
- **Explore** price distribution by tier via bar chart
- **Analyze** price-to-rating correlations via scatter plots
- **Track** brand dominance with model count charts

---

## Data Pipeline Details

### Input Schema

| Column | Type | Description |
|--------|------|-------------|
| Brand | object | Manufacturer name |
| Current Price | float64 | Current market price (local currency) |
| Original Price | float64 | Original MRP before discount |
| Discount Percentage | float64 | Calculated discount percentage |
| Rating | float64 | Average user rating (1-5) |
| Number OF Ratings | float64 | Total user reviews |
| Model Name | object | Product model identifier |
| Display Size | object | Screen size in inches (parsed to numeric) |
| Weight | object | Weight in grams (parsed to numeric) |

### Derived Features

| Feature | Description |
|---------|-------------|
| `price_tier` | Budget, Entry, Mid-Range, Premium, Luxury |
| `discount_category` | Small, Moderate, Large, Extreme Discount |
| `rating_category` | Poor, Fair, Good, Very Good, Excellent |
| `discount_amount` | Original Price - Current Price |
| `display_size_inches` | Numeric display size extracted from string |
| `weight_grams` | Average weight from range (e.g., "35 - 50 g") |
| `has_bluetooth` | Boolean flag for Bluetooth support |
| `has_touchscreen` | Boolean flag for touchscreen support |
| `value_score` | Rating normalized by price relative to median |
| `brand_popularity_score` | Percentile rank based on total ratings |

### Validation Rules

- **Negative Price Check**: Current and Original Price must be >= 0
- **Rating Range**: Rating must be between 0 and 5
- **Discount Range**: Discount Percentage must be between -100 and 100
- **Schema Enforcement**: All expected columns must be present with correct data types

---

## Future Work

- [ ] **ML Pipeline**: Add regression models for price prediction using engineered features
- [ ] **Data Versioning**: Implement DVC for tracking changes in processed datasets
- [ ] **Alerting**: Integrate Slack/email notifications for pipeline failures
- [ ] **API Layer**: Build REST API to serve feature store and predictions
- [ ] **Expanded Data Sources**: Scrape real-time data from e-commerce platforms
- [ ] **Monitoring**: Add data drift detection for production ML models

---


---

## Connect

**Live Demo:** https://dashboardpy-33ru9vmapuwcobxsrcybwk.streamlit.app/  


---

*Built with Python, Pandas, and Streamlit.*
