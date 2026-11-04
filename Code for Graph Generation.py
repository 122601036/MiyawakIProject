import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. INPUT DATASET (Exact extraction from l.pdf & q.pdf)
# ---------------------------------------------------------
sheet_data = [
    {"tree_id": "Tree_201", "species": "Terminalia bellirica", "rho": 0.76, "stems": [{"cbh": 5.0, "h": 2.15}]},
    {"tree_id": "Tree_202", "species": "Pongamia pinnata", "rho": 0.64, "stems": [{"cbh": 20.0, "h": 2.71}]},
    {"tree_id": "Tree_203", "species": "Cassia fistula", "rho": 0.96, "stems": [{"cbh": 20.0, "h": 3.28}]},
    {"tree_id": "Tree_204", "species": "Bauhinia purpurea", "rho": 0.72, "stems": [{"cbh": 12.0, "h": 3.40}]},
    {"tree_id": "Tree_205", "species": "Pongamia pinnata", "rho": 0.64, "stems": [{"cbh": 7.0, "h": 3.50}]},
    # Tree 206: Excluded (Tree Exist = No, Can be measured = No)
    {"tree_id": "Tree_207", "species": "Terminalia bellirica", "rho": 0.76, "stems": [{"cbh": 3.0, "h": 2.14}]},
    # Tree 208: Excluded (Can be measured = No)
    # Tree 209: Excluded (Can be measured = No)
    {"tree_id": "Tree_210", "species": "Cassia fistula", "rho": 0.96, "stems": [{"cbh": 20.0, "h": 6.60}]},
    {"tree_id": "Tree_211", "species": "Terminalia bellirica", "rho": 0.76, "stems": [{"cbh": 13.0, "h": 5.50}]},
    {"tree_id": "Tree_212", "species": "Terminalia bellirica", "rho": 0.76, "stems": [{"cbh": 10.0, "h": 3.13}]},
    {"tree_id": "Tree_213", "species": "Pongamia pinnata", "rho": 0.64, "stems": [{"cbh": 13.0, "h": 4.91}]},
    {"tree_id": "Tree_214", "species": "Swietenia mahagoni", "rho": 0.51, "stems": [{"cbh": 10.5, "h": 4.38}]},
    {"tree_id": "Tree_215", "species": "Terminalia bellirica", "rho": 0.76, "stems": [{"cbh": 25.0, "h": 6.48}]},
    {"tree_id": "Tree_216", "species": "Pongamia pinnata", "rho": 0.64, "stems": [{"cbh": 17.0, "h": 4.34}]},
    # Tree 217: Excluded (Can be measured = No)
    {"tree_id": "Tree_218", "species": "Bauhinia purpurea", "rho": 0.72, "stems": [{"cbh": 16.0, "h": 2.98}, {"cbh": 6.0, "h": 3.02}]}, # Multi-stem
    {"tree_id": "Tree_219", "species": "Terminalia bellirica", "rho": 0.76, "stems": [{"cbh": 5.0, "h": 1.65}]},
    {"tree_id": "Tree_220", "species": "Bauhinia purpurea", "rho": 0.72, "stems": [{"cbh": 19.0, "h": 3.02}]},
    {"tree_id": "Tree_221", "species": "Terminalia bellirica", "rho": 0.76, "stems": [{"cbh": 8.0, "h": 2.37}]},
    {"tree_id": "Tree_222", "species": "Pongamia pinnata", "rho": 0.64, "stems": [{"cbh": 10.0, "h": 4.08}]},
    {"tree_id": "Tree_223", "species": "Terminalia bellirica", "rho": 0.76, "stems": [{"cbh": 18.0, "h": 4.27}]},
    {"tree_id": "Tree_224", "species": "Terminalia bellirica", "rho": 0.76, "stems": [{"cbh": 4.0, "h": 2.13}]},
    {"tree_id": "Tree_225", "species": "Terminalia bellirica", "rho": 0.76, "stems": [{"cbh": 19.6, "h": 4.44}]}
]

df = pd.DataFrame(sheet_data)

# ---------------------------------------------------------
# 2. ALLOMETRIC EQUATION & SIMULATION
# ---------------------------------------------------------
def chave_2014_agb(rho, dbh, h):
    return 0.0673 * ((rho * (dbh ** 2) * h) ** 0.976)

NUM_DRAWS = 1000
np.random.seed(42)

tree_ids = []
means = []
medians = []
lower_errs = []
upper_errs = []

for _, row in df.iterrows():
    rho_mean = row['rho']
    tree_agb_draws = np.zeros(NUM_DRAWS)
    
    # Process each stem individually and sum per section 2 rules
    for stem in row['stems']:
        dbh_mean = stem['cbh'] / np.pi
        h_mean = stem['h']
        
        dbh_draws = np.maximum(stats.norm(loc=dbh_mean, scale=0.3).rvs(size=NUM_DRAWS), 0.1)
        h_draws = np.maximum(stats.norm(loc=h_mean, scale=0.8).rvs(size=NUM_DRAWS), 0.1)
        rho_draws = np.maximum(stats.norm(loc=rho_mean, scale=0.05).rvs(size=NUM_DRAWS), 0.05)
        
        tree_agb_draws += chave_2014_agb(rho_draws, dbh_draws, h_draws)
    
    mean_val = np.mean(tree_agb_draws)
    p2_5 = np.percentile(tree_agb_draws, 2.5)
    p50_0 = np.percentile(tree_agb_draws, 50.0)
    p97_5 = np.percentile(tree_agb_draws, 97.5)
    
    tree_ids.append(row['tree_id'])
    means.append(mean_val)
    medians.append(p50_0)
    lower_errs.append(mean_val - p2_5)
    upper_errs.append(p97_5 - mean_val)

# ---------------------------------------------------------
# 3. PLOTTING
# ---------------------------------------------------------
plt.figure(figsize=(14, 6))

plt.errorbar(
    tree_ids, 
    means, 
    yerr=[lower_errs, upper_errs], 
    fmt='o', 
    color='#1f77b4', 
    ecolor='#d62728', 
    elinewidth=1.5, 
    capsize=4, 
    capthick=1.5,
    markersize=6,
    label='Mean AGB with 95% Interval (2.5th–97.5th percentile)'
)

plt.plot(tree_ids, medians, 'x', color='#2ca02c', markersize=7, markeredgewidth=2, label='50th Percentile (Median)')

plt.xlabel('Tree ID', fontsize=12, fontweight='bold')
plt.ylabel('Above-Ground Biomass (kg)', fontsize=12, fontweight='bold')
plt.title('Part 3: Monte Carlo Uncertainty Analysis of Generic Chave AGB Estimates (N = 21 Trees Used)', fontsize=13, fontweight='bold', pad=15)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(loc='upper left', fontsize=10)
plt.tight_layout()

caption_text = f"Figure 1: Mean above-ground biomass (AGB in kg) per tree with 95% confidence intervals (2.5th to 97.5th percentiles) computed from N = {NUM_DRAWS:,} Monte Carlo simulation draws (4 trees excluded: 206 missing; 208, 209, 217 unmeasured; Tree 218 calculated as multi-stem)."
plt.figtext(0.5, -0.02, caption_text, wrap=True, horizontalalignment='center', fontsize=9.5, fontstyle='italic')

plt.savefig('l_sheet_part3_monte_carlo_agb_graph.png', dpi=300, bbox_inches='tight')
plt.show()
