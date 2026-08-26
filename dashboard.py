import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Smartwatch Analytics", layout="wide")
st.title("Smartwatch Market Analytics Dashboard")

# Load data
DATA_PATH = Path("data/processed/smartwatches_clean.csv")

try:
    df = pd.read_csv(DATA_PATH)
    st.success(f"Loaded {len(df)} smartwatch models")
except FileNotFoundError:
    st.error("Run pipeline.py first to generate data.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")
brand_filter = st.sidebar.multiselect("Select Brands", options=df['brand'].unique(), default=df['brand'].unique())
price_tier_filter = st.sidebar.multiselect("Price Tier", options=df['price_tier'].unique(), default=df['price_tier'].unique())

filtered_df = df[df['brand'].isin(brand_filter) & df['price_tier'].isin(price_tier_filter)]

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Models", len(filtered_df))
col2.metric("Average Price", f"${filtered_df['current_price'].mean():,.0f}")
col3.metric("Average Rating", f"{filtered_df['rating'].mean():.2f}")
col4.metric("Unique Brands", filtered_df['brand'].nunique())

# Row 2: Price Distribution
st.subheader("Price Distribution by Tier")
fig, ax = plt.subplots(figsize=(10, 4))
filtered_df['price_tier'].value_counts().sort_index().plot(kind='bar', color='skyblue', ax=ax)
ax.set_xlabel("Price Tier")
ax.set_ylabel("Count")
st.pyplot(fig)

# Row 3: Scatter Plot
st.subheader("Price vs. Rating")
fig2, ax2 = plt.subplots(figsize=(10, 5))
scatter = ax2.scatter(filtered_df['current_price'], filtered_df['rating'], 
                      c=pd.factorize(filtered_df['brand'])[0], alpha=0.6, cmap='viridis')
ax2.set_xlabel("Price ($)")
ax2.set_ylabel("Rating")
ax2.grid(alpha=0.3)
st.pyplot(fig2)

# Row 4: Top Brands
st.subheader("Top Brands by Model Count")
top_brands = filtered_df['brand'].value_counts().head(10)
fig3, ax3 = plt.subplots(figsize=(10, 4))
top_brands.plot(kind='bar', color='steelblue', ax=ax3)
ax3.set_xlabel("Brand")
ax3.set_ylabel("Number of Models")
plt.xticks(rotation=45)
st.pyplot(fig3)

st.caption("Data pipeline run completed. Dashboard is interactive.")
