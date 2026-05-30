# ============================================================
#  BANK MARKETING CAMPAIGN — EDA (Exploratory Data Analysis)
#  Author  : Mansour Mishwady
#  Tool    : Python
#  Dataset : Bank Marketing Campaign Data (11,162 records)
# ============================================================
#
#  TABLE OF CONTENTS
#  -----------------
#  STEP 1 : Import Libraries
#  STEP 2 : Load the Data
#  STEP 3 : First Look at the Data
#  STEP 4 : Data Cleaning
#  STEP 5 : Overview Dashboard (Target + Age + Balance + Duration)
#  STEP 6 : Job & Campaign Analysis
#  STEP 7 : Financial & Previous Campaign Analysis
#  STEP 8 : Key Insights Summary
# ============================================================


# ============================================================
# STEP 1 — IMPORT LIBRARIES
# ============================================================
# Think of libraries as toolboxes. We bring them in so we can
# use their ready-made functions instead of writing everything
# from scratch.

import pandas as pd           # For loading and working with tables (DataFrames)
import matplotlib.pyplot as plt  # For creating charts
import matplotlib
matplotlib.use('Agg')         # Tells matplotlib to save charts to files (not pop up a window)
import seaborn as sns         # Makes charts look nicer with less code
import warnings
warnings.filterwarnings('ignore')  # Hide unimportant warning messages

# Set a clean visual style for all charts
sns.set_theme(style="whitegrid", font_scale=1.1)

# Define our color palette — green = subscribed, red = not subscribed
GREEN  = "#2ecc71"
RED    = "#e74c3c"
BLUE   = "#2980b9"
ORANGE = "#e67e22"
PALETTE = {"yes": GREEN, "no": RED}


# ============================================================
# STEP 2 — LOAD THE DATA
# ============================================================
# pd.read_csv() reads a CSV file and turns it into a DataFrame.
# A DataFrame is like an Excel table — rows and columns.

df = pd.read_csv("C:\Users\mansour\Downloads\dataset\bank campaign 1\bank (1).csv")

print("✅ Data loaded successfully!")
print(f"   Rows    : {df.shape[0]:,}")   # shape[0] = number of rows
print(f"   Columns : {df.shape[1]}")     # shape[1] = number of columns


# ============================================================
# STEP 3 — FIRST LOOK AT THE DATA
# ============================================================

# --- 3a. See the first 5 rows ---
print("\n📋 First 5 rows of the dataset:")
print(df.head())

# --- 3b. Column names and data types ---
# int64  = whole numbers (e.g., age, balance)
# object = text / categories (e.g., job, marital)
print("\n📊 Column data types:")
print(df.dtypes)

# --- 3c. Summary statistics for numbers ---
# count  = how many values exist
# mean   = average
# std    = standard deviation (how spread out the values are)
# min/max = smallest and largest values
# 25%/50%/75% = quartiles (splitting data into 4 equal parts)
print("\n📈 Statistical Summary (numeric columns):")
print(df.describe())

# --- 3d. Check for missing values ---
# Missing values = empty cells. They can cause problems in analysis.
print("\n❓ Missing values per column:")
print(df.isnull().sum())
# Result: 0 in all columns — great, no missing data!

# --- 3e. Check the target column ---
# Our goal is to predict who will subscribe to a term deposit (deposit = yes/no)
print("\n🎯 Target Column — Deposit Subscription:")
print(df['deposit'].value_counts())


# ============================================================
# STEP 4 — DATA CLEANING
# ============================================================
# Even though there are no missing values, we still need to:
# 1. Create useful new columns (feature engineering)
# 2. Fix pdays (-1 means "not contacted before" — we'll clarify this)

# --- 4a. Create age groups ---
# pd.cut() divides a continuous number into labeled groups (bins)
df['age_group'] = pd.cut(
    df['age'],
    bins=[17, 25, 35, 45, 55, 65, 100],
    labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
)

# --- 4b. Create balance segments ---
df['balance_group'] = pd.cut(
    df['balance'],
    bins=[-7000, 0, 500, 1500, 5000, 82000],
    labels=['Negative', 'Low (0-500)', 'Medium (500-1.5k)', 'High (1.5k-5k)', 'Very High (5k+)']
)

# --- 4c. Convert duration to minutes (easier to understand than seconds) ---
df['duration_min'] = df['duration'] / 60

# --- 4d. Flag whether this client was previously contacted ---
# pdays = -1 means they were NEVER contacted before
df['was_contacted_before'] = df['pdays'].apply(lambda x: 'No' if x == -1 else 'Yes')
# lambda is a tiny one-line function. This one says:
# "If pdays is -1, write 'No', otherwise write 'Yes'"

print("\n✅ Data Cleaning Complete!")
print(f"   New columns added: age_group, balance_group, duration_min, was_contacted_before")


# ============================================================
# STEP 5 — OVERVIEW DASHBOARD
# ============================================================
# gridspec lets us build a grid of charts in one figure.
# We'll create 2 rows × 3 columns = 6 charts in one image.

import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(18, 10), facecolor="#f0f4f8")
fig.suptitle(
    "Bank Marketing Campaign — Overview Dashboard",
    fontsize=22, fontweight='bold', y=0.98, color="#2c3e50"
)
gs = fig.add_gridspec(2, 3, hspace=0.45, wspace=0.35,
                      left=0.06, right=0.97, top=0.91, bottom=0.08)

# ── Chart 1: Pie chart — Who subscribed? ─────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
counts = df['deposit'].value_counts()
ax1.pie(
    counts,
    labels=['No Deposit', 'Subscribed'],
    colors=[RED, GREEN],
    autopct='%1.1f%%',          # Show percentages
    startangle=90,
    wedgeprops=dict(edgecolor='white', linewidth=2)
)
ax1.set_title("Deposit Subscription Rate", fontweight='bold', pad=12)

# ── Chart 2: Histogram — Age distribution ────────────────────────
# A histogram shows how data is spread across ranges.
ax2 = fig.add_subplot(gs[0, 1])
for val, color in PALETTE.items():
    subset = df[df['deposit'] == val]['age']
    ax2.hist(subset, bins=20, alpha=0.65, color=color,
             label=val.capitalize(), edgecolor='white')
ax2.set_title("Age Distribution by Deposit", fontweight='bold')
ax2.set_xlabel("Age"); ax2.set_ylabel("Count")
ax2.legend(title="Subscribed?")

# ── Chart 3: Boxplot — Balance by deposit ────────────────────────
# A boxplot shows the median, spread, and outliers of a numeric column.
# We remove the top 5% to avoid extreme outliers squishing the chart.
ax3 = fig.add_subplot(gs[0, 2])
df_bal = df[df['balance'] < df['balance'].quantile(0.95)]
sns.boxplot(
    data=df_bal, x='deposit', y='balance',
    palette=PALETTE, ax=ax3, order=['no', 'yes'],
    width=0.5, linewidth=1.5
)
ax3.set_title("Balance by Deposit (excl. top 5% outliers)", fontweight='bold')
ax3.set_xlabel("Subscribed?"); ax3.set_ylabel("Balance (€)")
ax3.set_xticklabels(["No", "Yes"])

# ── Chart 4: Histogram — Call duration ───────────────────────────
ax4 = fig.add_subplot(gs[1, 0])
for val, color in PALETTE.items():
    subset = df[df['deposit'] == val]['duration_min']
    ax4.hist(subset, bins=25, alpha=0.65, color=color,
             label=val.capitalize(), edgecolor='white')
ax4.set_title("Call Duration by Deposit", fontweight='bold')
ax4.set_xlabel("Duration (minutes)"); ax4.set_ylabel("Count")
ax4.legend(title="Subscribed?")

# ── Chart 5: Bar chart — Marital status ──────────────────────────
ax5 = fig.add_subplot(gs[1, 1])
marital_dep = df.groupby(['marital', 'deposit']).size().unstack(fill_value=0)
marital_dep_pct = marital_dep.div(marital_dep.sum(axis=1), axis=0) * 100
x = range(len(marital_dep_pct))
w = 0.35
ax5.bar([i - w/2 for i in x], marital_dep_pct['no'], w, color=RED, label='No', edgecolor='white')
ax5.bar([i + w/2 for i in x], marital_dep_pct['yes'], w, color=GREEN, label='Yes', edgecolor='white')
ax5.set_xticks(list(x)); ax5.set_xticklabels(marital_dep_pct.index)
ax5.set_title("Subscription Rate by Marital Status", fontweight='bold')
ax5.set_ylabel("Percentage (%)"); ax5.legend(title="Subscribed?")

# ── Chart 6: Bar chart — Education level ─────────────────────────
ax6 = fig.add_subplot(gs[1, 2])
edu_dep = df.groupby(['education', 'deposit']).size().unstack(fill_value=0)
edu_dep_pct = edu_dep.div(edu_dep.sum(axis=1), axis=0) * 100
x = range(len(edu_dep_pct))
ax6.bar([i - w/2 for i in x], edu_dep_pct['no'], w, color=RED, label='No', edgecolor='white')
ax6.bar([i + w/2 for i in x], edu_dep_pct['yes'], w, color=GREEN, label='Yes', edgecolor='white')
ax6.set_xticks(list(x)); ax6.set_xticklabels(edu_dep_pct.index, rotation=15)
ax6.set_title("Subscription Rate by Education", fontweight='bold')
ax6.set_ylabel("Percentage (%)"); ax6.legend(title="Subscribed?")

plt.savefig("fig1_overview_dashboard.png", dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Figure 1 saved: fig1_overview_dashboard.png")


# ============================================================
# STEP 6 — JOB & CAMPAIGN ANALYSIS
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(18, 12), facecolor="#f0f4f8")
fig.suptitle(
    "Bank Marketing Campaign — Job & Campaign Analysis",
    fontsize=22, fontweight='bold', y=0.98, color="#2c3e50"
)
plt.subplots_adjust(hspace=0.45, wspace=0.35, left=0.07, right=0.97, top=0.91, bottom=0.08)

# ── Chart 1: Horizontal bar — Subscription rate by job ───────────
ax = axes[0, 0]
job_dep = df.groupby(['job', 'deposit']).size().unstack(fill_value=0)
job_dep['total'] = job_dep.sum(axis=1)
job_dep['yes_pct'] = job_dep['yes'] / job_dep['total'] * 100
job_dep_sorted = job_dep.sort_values('yes_pct', ascending=True)
bars = ax.barh(job_dep_sorted.index, job_dep_sorted['yes_pct'],
               color=BLUE, edgecolor='white', height=0.6)
ax.set_title("Subscription Rate by Job Type", fontweight='bold')
ax.set_xlabel("Subscription Rate (%)")
for bar, val in zip(bars, job_dep_sorted['yes_pct']):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f'{val:.1f}%', va='center', fontsize=9, fontweight='bold')
ax.set_xlim(0, 80)

# ── Chart 2: Bar chart — Monthly subscription rate ───────────────
ax = axes[0, 1]
month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
               'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
month_dep = df.groupby(['month', 'deposit']).size().unstack(fill_value=0)
month_dep = month_dep.reindex([m for m in month_order if m in month_dep.index])
month_dep['yes_pct'] = month_dep['yes'] / (month_dep['yes'] + month_dep['no']) * 100
colors_bar = [GREEN if v >= 50 else RED for v in month_dep['yes_pct']]
ax.bar(range(len(month_dep)), month_dep['yes_pct'],
       color=colors_bar, edgecolor='white', width=0.6)
ax.axhline(50, color='gray', linestyle='--', linewidth=1, alpha=0.7)
ax.set_xticks(range(len(month_dep)))
ax.set_xticklabels(month_dep.index, rotation=45)
ax.set_title("Subscription Rate by Month", fontweight='bold')
ax.set_ylabel("Subscription Rate (%)")
for i, val in enumerate(month_dep['yes_pct']):
    ax.text(i, val + 0.5, f'{val:.0f}%', ha='center', fontsize=8, fontweight='bold')

# ── Chart 3: Bar chart — Contact type ────────────────────────────
ax = axes[1, 0]
contact_dep = df.groupby(['contact', 'deposit']).size().unstack(fill_value=0)
contact_dep_pct = contact_dep.div(contact_dep.sum(axis=1), axis=0) * 100
x = range(len(contact_dep_pct))
w = 0.35
ax.bar([i - w/2 for i in x], contact_dep_pct['no'], w, color=RED, label='No', edgecolor='white')
ax.bar([i + w/2 for i in x], contact_dep_pct['yes'], w, color=GREEN, label='Yes', edgecolor='white')
ax.set_xticks(list(x)); ax.set_xticklabels(contact_dep_pct.index)
ax.set_title("Subscription Rate by Contact Type", fontweight='bold')
ax.set_ylabel("Percentage (%)"); ax.legend(title="Subscribed?")

# ── Chart 4: Line chart — Number of contacts vs. subscription ────
# As we contact people more times, does it help or hurt?
ax = axes[1, 1]
df_camp = df[df['campaign'] <= 15]
avg_by_camp = df_camp.groupby('campaign')['deposit'].apply(
    lambda x: (x == 'yes').mean() * 100
)
ax.plot(avg_by_camp.index.tolist(), avg_by_camp.values.tolist(),
        marker='o', color=BLUE, linewidth=2.5, markersize=7)
ax.fill_between(avg_by_camp.index.tolist(), avg_by_camp.values.tolist(),
                alpha=0.15, color=BLUE)
ax.set_title("Subscription Rate vs. Number of Contacts", fontweight='bold')
ax.set_xlabel("Number of Contacts in Campaign")
ax.set_ylabel("Subscription Rate (%)")

plt.savefig("fig2_job_campaign_analysis.png", dpi=150, bbox_inches='tight')
plt.close()
print("✅ Figure 2 saved: fig2_job_campaign_analysis.png")


# ============================================================
# STEP 7 — FINANCIAL & PREVIOUS CAMPAIGN ANALYSIS
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(18, 12), facecolor="#f0f4f8")
fig.suptitle(
    "Bank Marketing Campaign — Financial & Previous Campaign Analysis",
    fontsize=20, fontweight='bold', y=0.98, color="#2c3e50"
)
plt.subplots_adjust(hspace=0.45, wspace=0.35, left=0.07, right=0.97, top=0.91, bottom=0.08)

# ── Chart 1: Previous campaign outcome vs. subscription ──────────
ax = axes[0, 0]
pout_dep = df.groupby(['poutcome', 'deposit']).size().unstack(fill_value=0)
pout_dep_pct = pout_dep.div(pout_dep.sum(axis=1), axis=0) * 100
x = range(len(pout_dep_pct)); w = 0.35
ax.bar([i - w/2 for i in x], pout_dep_pct['no'], w, color=RED, label='No', edgecolor='white')
ax.bar([i + w/2 for i in x], pout_dep_pct['yes'], w, color=GREEN, label='Yes', edgecolor='white')
ax.set_xticks(list(x)); ax.set_xticklabels(pout_dep_pct.index)
ax.set_title("Subscription Rate by Previous Campaign Outcome", fontweight='bold')
ax.set_ylabel("Percentage (%)"); ax.legend(title="Subscribed?")

# ── Chart 2: Impact of loans and credit default ───────────────────
ax = axes[0, 1]
categories = ['housing', 'loan', 'default']
labels = ['Housing Loan', 'Personal Loan', 'Credit Default']
yes_rates, no_rates = [], []
for cat in categories:
    grp = df.groupby([cat, 'deposit']).size().unstack(fill_value=0)
    grp_pct = grp.div(grp.sum(axis=1), axis=0) * 100
    yes_rates.append(grp_pct.loc['yes', 'yes'] if 'yes' in grp_pct.index else 0)
    no_rates.append(grp_pct.loc['no', 'yes'] if 'no' in grp_pct.index else 0)
x = range(len(labels)); w = 0.35
ax.bar([i - w/2 for i in x], no_rates, w, color='#3498db', label='No Loan/Default', edgecolor='white')
ax.bar([i + w/2 for i in x], yes_rates, w, color=ORANGE, label='Has Loan/Default', edgecolor='white')
ax.set_xticks(list(x)); ax.set_xticklabels(labels)
ax.set_title("Subscription Rate: Loan & Default Impact", fontweight='bold')
ax.set_ylabel("Subscription Rate (%)"); ax.legend()

# ── Chart 3: Balance segments ─────────────────────────────────────
ax = axes[1, 0]
bal_dep = df.groupby(['balance_group', 'deposit'], observed=True).size().unstack(fill_value=0)
bal_dep_pct = bal_dep.div(bal_dep.sum(axis=1), axis=0) * 100
x = range(len(bal_dep_pct)); w = 0.35
ax.bar([i - w/2 for i in x], bal_dep_pct['no'], w, color=RED, label='No', edgecolor='white')
ax.bar([i + w/2 for i in x], bal_dep_pct['yes'], w, color=GREEN, label='Yes', edgecolor='white')
ax.set_xticks(list(x)); ax.set_xticklabels(bal_dep_pct.index, fontsize=9)
ax.set_title("Subscription Rate by Balance Segment", fontweight='bold')
ax.set_ylabel("Percentage (%)"); ax.legend(title="Subscribed?")

# ── Chart 4: Age groups ───────────────────────────────────────────
ax = axes[1, 1]
age_dep = df.groupby(['age_group', 'deposit'], observed=True).size().unstack(fill_value=0)
age_dep_pct = age_dep.div(age_dep.sum(axis=1), axis=0) * 100
colors_age = [GREEN if v >= 50 else ('#f39c12' if v >= 40 else RED)
              for v in age_dep_pct['yes']]
ax.bar(range(len(age_dep_pct)), age_dep_pct['yes'],
       color=colors_age, edgecolor='white', width=0.6)
ax.set_xticks(range(len(age_dep_pct)))
ax.set_xticklabels(age_dep_pct.index)
ax.set_title("Subscription Rate by Age Group", fontweight='bold')
ax.set_xlabel("Age Group"); ax.set_ylabel("Subscription Rate (%)")
for i, val in enumerate(age_dep_pct['yes']):
    ax.text(i, val + 0.5, f'{val:.0f}%', ha='center', fontsize=9, fontweight='bold')

plt.savefig("fig3_financial_analysis.png", dpi=150, bbox_inches='tight')
plt.close()
print("✅ Figure 3 saved: fig3_financial_analysis.png")


# ============================================================
# STEP 8 — KEY INSIGHTS SUMMARY
# ============================================================

print("""
╔══════════════════════════════════════════════════════════════╗
║         KEY INSIGHTS — BANK MARKETING CAMPAIGN EDA          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  1. OVERALL RATE                                             ║
║     • 47.4% of customers subscribed — nearly balanced data   ║
║                                                              ║
║  2. BEST JOB PROFILES                                        ║
║     • Students & Retired customers have the highest          ║
║       subscription rates (low financial pressure)            ║
║     • Blue-collar workers show the lowest rates              ║
║                                                              ║
║  3. BEST MONTHS TO CALL                                      ║
║     • March, September, October, December perform best       ║
║     • May has very high volume but poor conversion           ║
║                                                              ║
║  4. CALL DURATION MATTERS                                    ║
║     • Longer calls strongly correlate with subscriptions     ║
║     • Calls under 2 minutes rarely convert                   ║
║                                                              ║
║  5. PREVIOUS CAMPAIGN SUCCESS                                ║
║     • Clients who SUCCEEDED in a previous campaign are       ║
║       3-4x more likely to subscribe again                    ║
║                                                              ║
║  6. FINANCIAL STATUS                                         ║
║     • Higher balance → higher subscription rate              ║
║     • Having a housing loan reduces subscription likelihood  ║
║                                                              ║
║  7. AGE GROUPS                                               ║
║     • 18-25 and 65+ have the highest subscription rates      ║
║     • Middle-aged groups (36-55) are hardest to convert      ║
║                                                              ║
║  8. CONTACT TYPE                                             ║
║     • Cellular contact outperforms telephone                 ║
║     • Unknown contact type has poor conversion               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

print("🎉 EDA Complete! All figures saved.")
print("   Next Step: Open the PNG files to see your charts.")
print("   Then: Import them into Power BI for an interactive dashboard!")
