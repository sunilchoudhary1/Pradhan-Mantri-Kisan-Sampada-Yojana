import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'Pmksy1.csv'  # Update this if needed
df = pd.read_csv(file_path)

# Convert currency columns to numeric values (handling missing data)
df['Cost Of The Project (UOM:INR(IndianRupees))'] = pd.to_numeric(df['Cost Of The Project (UOM:INR(IndianRupees))'], errors='coerce')
df['Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))'] = pd.to_numeric(df['Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))'], errors='coerce')
df['Total Amount Of Grant Released (UOM:INR(IndianRupees))'] = pd.to_numeric(df['Total Amount Of Grant Released (UOM:INR(IndianRupees))'], errors='coerce')

# Sector-wise Investment Analysis
sector_wise = df.groupby('Sector')[['Cost Of The Project (UOM:INR(IndianRupees))',
                                    'Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))',
                                    'Total Amount Of Grant Released (UOM:INR(IndianRupees))']].sum()
sector_wise = sector_wise.sort_values(by='Cost Of The Project (UOM:INR(IndianRupees))', ascending=False)

# Plot Sector-wise Investment
plt.figure(figsize=(18, 8))
ax = sector_wise.plot(kind='bar', figsize=(18, 8), colormap='viridis')
plt.title("Sector-Wise Investment in PMKSY Projects", fontsize=14)
plt.xlabel("Sector", fontsize=12)
plt.ylabel("Amount (INR Crores)", fontsize=12)
plt.xticks(rotation=30, ha='right', fontsize=10)
plt.legend(["Total Project Cost", "Approved Grant", "Grant Released"], fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()  # Adjust layout to prevent cut-off labels

# Adding value labels on top of bars
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=9, rotation=90)
plt.show()

# State-wise Investment Analysis
state_wise = df.groupby('State')[['Cost Of The Project (UOM:INR(IndianRupees))',
                                  'Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))',
                                  'Total Amount Of Grant Released (UOM:INR(IndianRupees))']].sum()
state_wise = state_wise.sort_values(by='Cost Of The Project (UOM:INR(IndianRupees))', ascending=False)

# Plot State-wise Investment
plt.figure(figsize=(18, 8))
ax = state_wise.plot(kind='bar', figsize=(18, 8), colormap='coolwarm')
plt.title("State-Wise Investment in PMKSY Projects", fontsize=14)
plt.xlabel("State", fontsize=12)
plt.ylabel("Amount (INR Crores)", fontsize=12)
plt.xticks(rotation=30, ha='right', fontsize=10)
plt.legend(["Total Project Cost", "Approved Grant", "Grant Released"], fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# Adding value labels on top of bars
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=9, rotation=90)
plt.show()

# Funding Gap Analysis
funding_gap = df.groupby('Sector')[['Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))',
                                    'Total Amount Of Grant Released (UOM:INR(IndianRupees))']].sum()
funding_gap['Funding Gap'] = funding_gap['Approved Amount Of Grant-In-Aid (UOM:INR(IndianRupees))'] - funding_gap['Total Amount Of Grant Released (UOM:INR(IndianRupees))']
funding_gap = funding_gap.sort_values(by='Funding Gap', ascending=False)

# Plot Funding Gaps
plt.figure(figsize=(18, 8))
ax = sns.barplot(x=funding_gap.index, y=funding_gap['Funding Gap'], palette='coolwarm')
plt.title("Funding Gap Analysis Across Sectors", fontsize=14)
plt.xlabel("Sector", fontsize=12)
plt.ylabel("Funding Gap (INR Crores)", fontsize=12)
plt.xticks(rotation=30, ha='right', fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# Adding value labels on bars
for p in ax.patches:
    ax.annotate(f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=9, rotation=90)
plt.show()

# Display summarized state-wise and sector-wise funding data
print("\nState-wise Investment Summary:")
print(state_wise.head())
print("\nSector-wise Investment Summary:")
print(sector_wise.head())
print("\nFunding Gap Analysis:")
print(funding_gap.head())
