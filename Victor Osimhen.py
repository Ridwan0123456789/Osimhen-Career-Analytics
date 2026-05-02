# =============================================================
# VICTOR OSIMHEN — CAREER ANALYTICS
# Author: Abdulkadri Ridwan
# Data Source: FBref.com
# Description: End-to-end analysis of Osimhen's domestic league
#              career across 10 seasons and 5 clubs
# Tools: Python | pandas | matplotlib | seaborn
# =============================================================


# ── SECTION 1: IMPORT LIBRARIES ──────────────────────────────
# pandas handles data — think of it as Excel but in code
# matplotlib is our basic drawing tool for charts
# seaborn builds on matplotlib and makes charts look professional
# os allows us to create folders and manage file paths

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ── SECTION 2: LOAD DATA ──────────────────────────────────────
# Read the Minutes Per Goal sheet from our Excel file
# na_values tells pandas to treat "N/A" text as missing data
# so it can handle them properly in calculations

df_mpg = pd.read_excel(
    r"C:\Users\phili\PycharmProjects\VO excel table(New).xlsx",
    sheet_name="Minutes Per Goal",
    na_values=["N/A"]
)

# Read the Shooting sheet from the same Excel file
df_shooting = pd.read_excel(
    r"C:\Users\phili\PycharmProjects\VO excel table(New).xlsx",
    sheet_name="Shooting",
    na_values=["N/A"]
)

# Confirm both sheets loaded correctly
print("Minutes Per Goal shape:", df_mpg.shape)
print("Shooting shape:", df_shooting.shape)


# ── SECTION 3: CLEAN DATA ─────────────────────────────────────

# Filter complete seasons only — exclude ongoing 2025-2026
# to avoid skewing calculations with incomplete data
df_mpg_complete = df_mpg[df_mpg["Status"] == "Complete"]

# For shooting — remove rows with missing SoT% or G/SoT values
# These are seasons where FBref had no shooting data recorded
df_shooting_clean = df_shooting.dropna(subset=["SoT%", "G/SoT"])

# Remove ongoing season from shooting data
df_shooting_clean = df_shooting_clean[
    df_shooting_clean["Season"] != "2025-2026"
].copy()

# Add Season_Order column so Power BI sorts seasons correctly
# Without this Power BI sorts alphabetically not chronologically
df_shooting_clean["Season_Order"] = range(1, len(df_shooting_clean) + 1)

# Rename columns to audience-friendly labels for Power BI
df_shooting_clean = df_shooting_clean.rename(columns={
    "SoT%": "Shot Accuracy %",
    "G/SoT": "Goals per Shot on Target"
})

print("\nComplete seasons:", len(df_mpg_complete))
print("Shooting seasons with complete data:", len(df_shooting_clean))


# ── SECTION 4: ADD CAREER PHASE COLUMN ───────────────────────
# This function assigns each season to one of three career phases
# apply() runs this function automatically on every row
# in the Season column

def assign_phase(season):
    if season in ["2016 - 2017", "2017 - 2018",
                  "2018 - 2019", "2019 - 2020"]:
        return "Development"
    elif season in ["2020 - 2021", "2021 - 2022"]:
        return "Transition"
    elif season in ["2022 - 2023", "2023 - 2024",
                    "2024 - 2025"]:
        return "Elite Peak"
    else:
        return "Ongoing"


df_mpg["Phase"] = df_mpg["Season"].apply(assign_phase)

# Confirm Phase column looks correct
print("\nSeason to Phase mapping:")
print(df_mpg[["Season", "Phase"]])


# ── SECTION 5: CALCULATE CAREER PHASE AVERAGES ───────────────
# Split completed seasons into three phases for comparison
# skipna=True tells Python to ignore N/A values when calculating

df_development = df_mpg_complete[df_mpg_complete["Season"].isin([
    "2016 - 2017", "2017 - 2018",
    "2018 - 2019", "2019 - 2020"])]

df_transition = df_mpg_complete[df_mpg_complete["Season"].isin([
    "2020 - 2021", "2021 - 2022"])]

df_elite = df_mpg_complete[df_mpg_complete["Season"].isin([
    "2022 - 2023", "2023 - 2024",
    "2024 - 2025"])]

avg_dev = df_development["Mins_Per_Goal_Calc"].mean(skipna=True)
avg_trans = df_transition["Mins_Per_Goal_Calc"].mean(skipna=True)
avg_elite = df_elite["Mins_Per_Goal_Calc"].mean(skipna=True)
avg_overall = df_mpg_complete["Mins_Per_Goal_Calc"].mean(skipna=True)

print("\n--- Career Phase Averages ---")
print(f"Overall career average:   {round(avg_overall, 1)} mins/goal")
print(f"Development phase average: {round(avg_dev, 1)} mins/goal")
print(f"Transition phase average:  {round(avg_trans, 1)} mins/goal")
print(f"Elite Peak phase average:  {round(avg_elite, 1)} mins/goal")
print(f"Efficiency improvement (Development to Elite Peak): "
      f"{round(avg_dev - avg_elite, 1)} minutes")


# ── SECTION 6: EXPORT CLEAN DATA FOR POWER BI ────────────────
# Export as CSV — Power BI reads CSV cleanly without formula issues
# index=False removes the row numbers Python adds automatically

df_mpg.to_csv(
    r"C:\Users\phili\PycharmProjects\VO_Minutes_Per_Goal.csv",
    index=False
)

df_shooting_clean.to_csv(
    r"C:\Users\phili\PycharmProjects\VO_Shooting.csv",
    index=False
)

print("\nBoth CSV files exported successfully")
print(f"Minutes Per Goal rows: {len(df_mpg)}")
print(f"Shooting rows: {len(df_shooting_clean)}")


# ── SECTION 7: CREATE OUTPUT FOLDER FOR CHARTS ───────────────
# os.makedirs creates a folder if it doesn't already exist
# exist_ok=True means it won't error if folder already exists

output_folder = r"C:\Users\phili\PycharmProjects\Osimhen_Charts"
os.makedirs(output_folder, exist_ok=True)


# ── SECTION 8: CHART 1 — CAREER PHASES BAR CHART ─────────────
# This chart shows the average minutes per goal across
# three career phases — the staircase pattern of improvement

df_phases = pd.DataFrame({
    "Phase": ["Development", "Transition", "Elite Peak"],
    "Avg_Mins_Per_Goal": [round(avg_dev, 1),
                          round(avg_trans, 1),
                          round(avg_elite, 1)]
})

plt.figure(figsize=(10, 6))
sns.barplot(data=df_phases,
            x="Phase",
            y="Avg_Mins_Per_Goal",
            palette="Blues_d")

plt.title("Osimhen Career Efficiency By Phase\nAverage Minutes Per Goal",
          fontsize=14, fontweight="bold")
plt.xlabel("Career Phase", fontsize=12)
plt.ylabel("Avg Minutes Per Goal (Lower = Better)", fontsize=12)

# Add value labels on top of each bar for immediate readability
for i, row in df_phases.iterrows():
    plt.text(i, row["Avg_Mins_Per_Goal"] - 8,
             str(row["Avg_Mins_Per_Goal"]),
             ha="center", fontsize=12,
             fontweight="bold", color="white")

plt.tight_layout()

# dpi=300 makes it high resolution — important for portfolio
plt.savefig(os.path.join(output_folder, "01_Career_Phases.png"),
            dpi=300, bbox_inches="tight")
plt.close()
print("\nChart 1 saved — Career Phases")


# ── SECTION 9: CHART 2 — SEASON BY SEASON TREND ──────────────
# This line chart shows the full career trend chronologically
# revealing the bounce-back pattern after every quiet season

df_trend = df_mpg[df_mpg["Mins_Per_Goal_Calc"].notna()]
df_trend = df_trend[df_trend["Status"] == "Complete"]

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_trend,
             x="Season",
             y="Mins_Per_Goal_Calc",
             marker="o",
             linewidth=2.5,
             color="steelblue")

# Highlight ongoing season with different colour
# so readers know it is not directly comparable
ongoing = df_mpg[df_mpg["Status"] == "Ongoing"]
plt.scatter(ongoing["Season"],
            ongoing["Mins_Per_Goal_Calc"],
            color="orange",
            zorder=5,
            s=100,
            label="Ongoing Season")

plt.title("Osimhen Season By Season Efficiency\nMinutes Per Goal Trend",
          fontsize=14, fontweight="bold")
plt.xlabel("Season", fontsize=12)
plt.ylabel("Minutes Per Goal (Lower = Better)", fontsize=12)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(output_folder, "02_Season_Trend.png"),
            dpi=300, bbox_inches="tight")
plt.close()
print("Chart 2 saved — Season Trend")


# ── SECTION 10: CHART 3 — FINISHING QUALITY ──────────────────
# Dual axis chart showing shot accuracy and conversion rate
# together — two dimensions of finishing quality in one visual
# twinx() creates a second y-axis sharing the same x-axis

fig, ax1 = plt.subplots(figsize=(12, 6))

color1 = "steelblue"
ax1.set_xlabel("Season", fontsize=12)
ax1.set_ylabel("Shot Accuracy (%)", color=color1, fontsize=12)
ax1.plot(df_shooting_clean["Season"],
         df_shooting_clean["Shot Accuracy %"],
         color=color1,
         marker="o",
         linewidth=2.5,
         label="Shot Accuracy %")
ax1.tick_params(axis="y", labelcolor=color1)
ax1.tick_params(axis="x", rotation=45)

# Second line on right y-axis
ax2 = ax1.twinx()
color2 = "darkorange"
ax2.set_ylabel("Goals per Shot on Target",
               color=color2, fontsize=12)
ax2.plot(df_shooting_clean["Season"],
         df_shooting_clean["Goals per Shot on Target"],
         color=color2,
         marker="s",
         linewidth=2.5,
         linestyle="--",
         label="Goals per Shot on Target")
ax2.tick_params(axis="y", labelcolor=color2)

plt.title("Osimhen Finishing Quality By Season\nShot Accuracy vs Conversion Rate",
          fontsize=14, fontweight="bold")

# Combine both line labels into one legend box
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.tight_layout()

plt.savefig(os.path.join(output_folder, "03_Finishing_Quality.png"),
            dpi=300, bbox_inches="tight")
plt.close()
print("Chart 3 saved — Finishing Quality")

print("\nAll charts exported to:", output_folder)
print("\nAnalysis complete.")