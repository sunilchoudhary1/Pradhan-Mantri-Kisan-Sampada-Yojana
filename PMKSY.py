import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'Pmksy1.csv'
df = pd.read_csv(file_path)

# Convert currency columns to numeric
df['Cost Of The Project (UOM:INR(IndianRupees))'] = pd.to_numeric(df['Cost Of The Project (UOM:INR(IndianRupees))'], errors='coerce')
df['Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))'] = pd.to_numeric(df['Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))'], errors='coerce')
df['Total Amount Of Grant Released (UOM:INR(IndianRupees))'] = pd.to_numeric(df['Total Amount Of Grant Released (UOM:INR(IndianRupees))'], errors='coerce')

# -------------------------------------
# Sector-wise Investment Analysis
sector_wise = df.groupby('Sector')[[
    'Cost Of The Project (UOM:INR(IndianRupees))',
    'Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))',
    'Total Amount Of Grant Released (UOM:INR(IndianRupees))'
]].sum().sort_values(by='Cost Of The Project (UOM:INR(IndianRupees))', ascending=False)

# Plot Sector-wise Investment
ax = sector_wise.plot(kind='bar', figsize=(18, 8), colormap='viridis')
plt.title("Sector-Wise Investment in PMKSY Projects", fontsize=14)
plt.xlabel("Sector", fontsize=12)
plt.ylabel("Amount (INR Crores)", fontsize=12)
plt.xticks(rotation=30, ha='right', fontsize=10)
plt.legend(["Total Project Cost", "Approved Grant", "Grant Released"], fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=9, rotation=90)
plt.show()

# -------------------------------------
# State-wise Investment Analysis
state_wise = df.groupby('State')[[
    'Cost Of The Project (UOM:INR(IndianRupees))',
    'Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))',
    'Total Amount Of Grant Released (UOM:INR(IndianRupees))'
]].sum().sort_values(by='Cost Of The Project (UOM:INR(IndianRupees))', ascending=False)

# Plot State-wise Investment
ax = state_wise.plot(kind='bar', figsize=(18, 8), colormap='coolwarm')
plt.title("State-Wise Investment in PMKSY Projects", fontsize=14)
plt.xlabel("State", fontsize=12)
plt.ylabel("Amount (INR Crores)", fontsize=12)
plt.xticks(rotation=30, ha='right', fontsize=10)
plt.legend(["Total Project Cost", "Approved Grant", "Grant Released"], fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=9, rotation=90)
plt.show()

# -------------------------------------
# Funding Gap Analysis
funding_gap = df.groupby('Sector')[[
    'Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))',
    'Total Amount Of Grant Released (UOM:INR(IndianRupees))'
]].sum()
funding_gap['Funding Gap'] = funding_gap['Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))'] - funding_gap['Total Amount Of Grant Released (UOM:INR(IndianRupees))']
funding_gap = funding_gap.sort_values(by='Funding Gap', ascending=False)

# Plot Funding Gaps
ax = sns.barplot(x=funding_gap.index, y=funding_gap['Funding Gap'], palette='coolwarm')
plt.title("Funding Gap Analysis Across Sectors", fontsize=14)
plt.xlabel("Sector", fontsize=12)
plt.ylabel("Funding Gap (INR Crores)", fontsize=12)
plt.xticks(rotation=30, ha='right', fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=9, rotation=90)
plt.show()

# -------------------------------------
# NEW: State-wise Cost of Projects Not Commercially Started Yet
df['Physical Progress Of The Project'] = df['Physical Progress Of The Project'].str.lower()
not_started_df = df[df['Physical Progress Of The Project'].str.contains('progress|not started|under implementation|under construction', na=False)]

not_started_statewise = not_started_df.groupby('State')['Cost Of The Project (UOM:INR(IndianRupees))'].sum().sort_values(ascending=False)

# Plot it
ax = not_started_statewise.plot(kind='bar', figsize=(18, 8), color='orange')
plt.title("State-wise Total Cost of Projects Not Commercially Started Yet", fontsize=14)
plt.xlabel("State", fontsize=12)
plt.ylabel("Cost of Incomplete Projects (INR Crores)", fontsize=12)
plt.xticks(rotation=30, ha='right', fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=9, rotation=90)
plt.show()

# -------------------------------------
# Print Summaries
print("\nState-wise Investment Summary:")
print(state_wise.head())

print("\nSector-wise Investment Summary:")
print(sector_wise.head())

print("\nFunding Gap Analysis:")
print(funding_gap.head())

print("\nState-wise Cost of Projects Not Yet Commercially Started:")
print(not_started_statewise.head())
