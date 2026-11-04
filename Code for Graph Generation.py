import numpy as np
import pandas as pd
from scipy import stats

# ---------------------------------------------------------
# 1. INPUT DATASET (Group 5_1 Measured Trees 201 to 225)
# ---------------------------------------------------------
raw_data = [
    {"tree_id": "Tree_201", "species": "Adenanthera pavonina", "cbh": 14.5, "height": 4.2, "rho": 0.88},
    {"tree_id": "Tree_202", "species": "Albizia lebbeck", "cbh": 18.2, "height": 5.1, "rho": 0.80},
    {"tree_id": "Tree_203", "species": "Alstonia scholaris", "cbh": 11.0, "height": 3.8, "rho": 0.44},
    {"tree_id": "Tree_204", "species": "Azadirachta indica", "cbh": 22.0, "height": 6.0, "rho": 0.66},
    {"tree_id": "Tree_205", "species": "Bambusa vulgaris", "cbh": 8.5, "height": 4.0, "rho": 0.77},
    {"tree_id": "Tree_206", "species": "Bauhinia purpurea", "cbh": 15.0, "height": 4.5, "rho": 0.72},
    {"tree_id": "Tree_208", "species": "Bridelia retusa", "cbh": 12.8, "height": 3.9, "rho": 0.50},
    {"tree_id": "Tree_209", "species": "Butea monosperma", "cbh": 19.4, "height": 5.5, "rho": 0.56},
    {"tree_id": "Tree_210", "species": "Cascabela thevetia", "cbh": 9.2, "height": 2.8, "rho": 0.72},
    {"tree_id": "Tree_212", "species": "Cassia fistula", "cbh": 16.5, "height": 4.8, "rho": 0.96},
    {"tree_id": "Tree_214", "species": "Dalbergia sissoo", "cbh": 21.0, "height": 5.8, "rho": 0.76},
    {"tree_id": "Tree_215", "species": "Delonix regia", "cbh": 25.0, "height": 6.5, "rho": 0.80},
    {"tree_id": "Tree_216", "species": "Gliricidia sepium", "cbh": 13.0, "height": 4.1, "rho": 0.74},
    {"tree_id": "Tree_217", "species": "Gmelina arborea", "cbh": 28.0, "height": 7.2, "rho": 0.56},
    {"tree_id": "Tree_218", "species": "Lagerstroemia speciosa", "cbh": 17.2, "height": 5.0, "rho": 0.64},
    {"tree_id": "Tree_220", "species": "Mimusops elengi", "cbh": 14.0, "height": 4.3, "rho": 0.80},
    {"tree_id": "Tree_221", "species": "Phyllanthus emblica", "cbh": 10.5, "height": 3.5, "rho": 0.68},
    {"tree_id": "Tree_222", "species": "Polyalthia longifolia", "cbh": 16.0, "height": 5.2, "rho": 0.59},
    {"tree_id": "Tree_223", "species": "Pongamia pinnata", "cbh": 20.1, "height": 5.7, "rho": 0.64},
    {"tree_id": "Tree_224", "species": "Prosopis cineraria", "cbh": 18.0, "height": 5.0, "rho": 0.663},
    {"tree_id": "Tree_225", "species": "Psidium guajava", "cbh": 11.8, "height": 3.6, "rho": 0.60}
]

df = pd.DataFrame(raw_data)

# ---------------------------------------------------------
# 2. CHAVE ET AL. (2014) ALLOMETRIC EQUATION
# ---------------------------------------------------------
def chave_2014_agb(rho, dbh, h):
    """
    Computes Above-Ground Biomass (kg) using Chave et al. (2014):
    AGB = 0.0673 * (rho * DBH^2 * H)^0.976
    - rho: Wood density (g/cm^3)
    - DBH: Diameter at Breast Height (cm)
    - H: Tree Height (m)
    """
    return 0.0673 * ((rho * (dbh ** 2) * h) ** 0.976)

# ---------------------------------------------------------
# 3. MONTE CARLO SIMULATION WITH NUMPY & SCIPY
# ---------------------------------------------------------
NUM_DRAWS = 1000  # Number of simulation draws
np.random.seed(42)  # For reproducible results

results = []

for _, row in df.iterrows():
    # Convert CBH (cm) to DBH (cm)
    dbh_mean = row['cbh'] / np.pi
    h_mean = row['height']
    rho_mean = row['rho']
    
    # 1. DBH ~ Normal(mean, 0.3) using scipy.stats
    dbh_dist = stats.norm(loc=dbh_mean, scale=0.3)
    dbh_draws = np.maximum(dbh_dist.rvs(size=NUM_DRAWS), 0.1)
    
    # 2. H ~ Normal(mean, 0.8) using scipy.stats
    h_dist = stats.norm(loc=h_mean, scale=0.8)
    h_draws = np.maximum(h_dist.rvs(size=NUM_DRAWS), 0.1)
    
    # 3. Wood Density ~ Normal(mean, 0.05) using scipy.stats
    rho_dist = stats.norm(loc=rho_mean, scale=0.05)
    rho_draws = np.maximum(rho_dist.rvs(size=NUM_DRAWS), 0.05)
    
    # Run 1,000 Chave AGB draws
    agb_draws = chave_2014_agb(rho_draws, dbh_draws, h_draws)
    
    # Calculate Mean, 2.5th, 50th, and 97.5th Percentiles
    mean_val = np.mean(agb_draws)
    p2_5 = np.percentile(agb_draws, 2.5)
    p50_0 = np.percentile(agb_draws, 50.0)  # Median
    p97_5 = np.percentile(agb_draws, 97.5)
    
    results.append({
        "Tree ID": row['tree_id'],
        "Species": row['species'],
        "DBH Mean (cm)": round(dbh_mean, 2),
        "Height (m)": row['height'],
        "Mean AGB (kg)": round(mean_val, 2),
        "2.5th Pct (kg)": round(p2_5, 2),
        "50th Pct / Median (kg)": round(p50_0, 2),
        "97.5th Pct (kg)": round(p97_5, 2),
        "95% CI Range (kg)": f"[{round(p2_5, 2)}, {round(p97_5, 2)}]"
    })

# ---------------------------------------------------------
# 4. OUTPUT SUMMARY TABLE
# ---------------------------------------------------------
summary_df = pd.DataFrame(results)

print("=== MONTE CARLO UNCERTAINTY ANALYSIS RESULTS (N=1,000 DRAWS) ===")
print(summary_df.to_string(index=False))

# Calculate total stand biomass percentiles across all 21 trees
total_agb_draws = np.zeros(NUM_DRAWS)
for _, row in df.iterrows():
    dbh_mean = row['cbh'] / np.pi
    dbh_draws = np.maximum(stats.norm(loc=dbh_mean, scale=0.3).rvs(size=NUM_DRAWS), 0.1)
    h_draws = np.maximum(stats.norm(loc=row['height'], scale=0.8).rvs(size=NUM_DRAWS), 0.1)
    rho_draws = np.maximum(stats.norm(loc=row['rho'], scale=0.05).rvs(size=NUM_DRAWS), 0.05)
    total_agb_draws += chave_2014_agb(rho_draws, dbh_draws, h_draws)

print("\n=== TOTAL STAND AGB PERCENTILES (21 MEASURED TREES) ===")
print(f"Mean Stand AGB:    {np.mean(total_agb_draws):.2f} kg")
print(f"2.5th Percentile:  {np.percentile(total_agb_draws, 2.5):.2f} kg")
print(f"50th Percentile:   {np.percentile(total_agb_draws, 50.0):.2f} kg")
print(f"97.5th Percentile: {np.percentile(total_agb_draws, 97.5):.2f} kg")
