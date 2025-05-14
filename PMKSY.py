import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# -----------------------------
# Load and clean main dataset
# -----------------------------
file_path = 'Pmksy1.csv'
df = pd.read_csv(file_path)

# Convert currency columns to numeric
df['Cost Of The Project (UOM:INR(IndianRupees))'] = pd.to_numeric(df['Cost Of The Project (UOM:INR(IndianRupees))'], errors='coerce')
df['Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))'] = pd.to_numeric(df['Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))'], errors='coerce')
df['Total Amount Of Grant Released (UOM:INR(IndianRupees))'] = pd.to_numeric(df['Total Amount Of Grant Released (UOM:INR(IndianRupees))'], errors='coerce')

# -----------------------------
# Sector-wise Investment Analysis
# -----------------------------
sector_wise = df.groupby('Sector')[[
    'Cost Of The Project (UOM:INR(IndianRupees))',
    'Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))',
    'Total Amount Of Grant Released (UOM:INR(IndianRupees))'
]].sum().sort_values(by='Cost Of The Project (UOM:INR(IndianRupees))', ascending=False)

ax = sector_wise.plot(kind='bar', figsize=(18, 8), colormap='viridis')
plt.title("Sector-Wise Investment in PMKSY Projects", fontsize=14)
plt.xlabel("Sector")
plt.ylabel("Amount (INR Crores)")
plt.xticks(rotation=30, ha='right')
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=9, rotation=90)
plt.show()

# -----------------------------
# State-wise Investment Analysis
# -----------------------------
state_wise = df.groupby('State')[[
    'Cost Of The Project (UOM:INR(IndianRupees))',
    'Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))',
    'Total Amount Of Grant Released (UOM:INR(IndianRupees))'
]].sum().sort_values(by='Cost Of The Project (UOM:INR(IndianRupees))', ascending=False)

ax = state_wise.plot(kind='bar', figsize=(18, 8), colormap='coolwarm')
plt.title("State-Wise Investment in PMKSY Projects", fontsize=14)
plt.xlabel("State")
plt.ylabel("Amount (INR Crores)")
plt.xticks(rotation=30, ha='right')
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=9, rotation=90)
plt.show()

# -----------------------------
# Funding Gap Analysis
# -----------------------------
funding_gap = df.groupby('Sector')[[
    'Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))',
    'Total Amount Of Grant Released (UOM:INR(IndianRupees))'
]].sum()
funding_gap['Funding Gap'] = funding_gap['Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))'] - funding_gap['Total Amount Of Grant Released (UOM:INR(IndianRupees))']
funding_gap = funding_gap.sort_values(by='Funding Gap', ascending=False)

ax = sns.barplot(x=funding_gap.index, y=funding_gap['Funding Gap'], hue=funding_gap.index, palette='coolwarm', legend=False)
plt.title("Funding Gap Analysis Across Sectors")
plt.xlabel("Sector")
plt.ylabel("Funding Gap (INR Crores)")
plt.xticks(rotation=30, ha='right')
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=9, rotation=90)
plt.show()

# -----------------------------
# Projects Not Commercially Started
# -----------------------------
df['Physical Progress Of The Project'] = df['Physical Progress Of The Project'].str.lower()
not_started_df = df[df['Physical Progress Of The Project'].str.contains('progress|not started|under implementation|under construction', na=False)]
not_started_statewise = not_started_df.groupby('State')['Cost Of The Project (UOM:INR(IndianRupees))'].sum().sort_values(ascending=False)

ax = not_started_statewise.plot(kind='bar', figsize=(18, 8), color='orange')
plt.title("State-wise Total Cost of Projects Not Commercially Started Yet")
plt.xlabel("State")
plt.ylabel("Cost of Incomplete Projects (INR Crores)")
plt.xticks(rotation=30, ha='right')
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=9, rotation=90)
plt.show()

# -----------------------------
# Geospatial Heatmap
# -----------------------------
map_data = df.groupby('State')[[
    'Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))',
    'Total Amount Of Grant Released (UOM:INR(IndianRupees))'
]].sum().reset_index()
map_data.rename(columns={
    'Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))': 'Approved_Amount',
    'Total Amount Of Grant Released (UOM:INR(IndianRupees))': 'Released_Amount'
}, inplace=True)

# Normalize case and spacing for proper matching
map_data['State'] = map_data['State'].str.strip().str.lower()

# Load India shapefile
map_df = gpd.read_file('gadm41_IND_1.shp')
map_df['NAME_1'] = map_df['NAME_1'].str.strip().str.lower()

# Merge with shapefile
merged = map_df.merge(map_data, left_on='NAME_1', right_on='State')

# Drop invalid geometries
merged = merged[merged.is_valid & ~merged.is_empty & merged['geometry'].notnull()]

# Calculate disbursement percentage
merged['Disbursement %'] = (merged['Released_Amount'] / merged['Approved_Amount']) * 100

# Plot heatmap
ax = merged.plot(column='Disbursement %',
                 cmap='YlOrRd',
                 legend=True,
                 figsize=(12, 8),
                 edgecolor='black')
ax.set_title('PMKSY Disbursement Percentage by State')
ax.set_aspect('auto')
plt.axis('off')
plt.show()

# -----------------------------
# Summary Print
# -----------------------------
print("\nState-wise Investment Summary:")
print(state_wise.head())

print("\nSector-wise Investment Summary:")
print(sector_wise.head())

print("\nFunding Gap Analysis:")
print(funding_gap.head())

print("\nState-wise Cost of Projects Not Yet Commercially Started:")
print(not_started_statewise.head())
