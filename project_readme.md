# Miyawaki Forest Biomass & Carbon Sequestration Analysis — Group 5_1

**Course:** Ecology and Environment (ES1010)  
**Institution:** Indian Institute of Technology Palakkad (IIT Palakkad)  
**Submission Date:** Saturday, 7 November 2026  

---

## 📌 Repository Overview

This repository contains the complete dataset, mathematical calculations, Monte Carlo simulation models, and analysis files for **Group 5_1**'s evaluation of a 5-year-old Miyawaki forest plot.

The analysis evaluates above-ground biomass ($\text{AGB}$) using generic vs. species-specific allometric models, calculates national $\text{CO}_2$ offset feasibility, and quantifies measurement uncertainty through 1,000 Monte Carlo sampling draws per tree.

---

## 👥 Group Roster & Roles (Group ID: 5_1)

| Roll Number | Name | Primary Contribution |
| :--- | :--- | :--- |
| `102601001` | **ABHISHEK CHOUDHARY** | Field Data Collection & Biomass Analysis |
| `122601036` | **RIDHWIMAN GAYEN** | Uncertainty Simulation & Code Scripting |
| `132601008` | **AVANI KIRAN NAIK** | Field Survey & Data Cleaning |
| `132601037` | **NISHOK A** | Field Measurement & Carbon Scaling Calculations |
| `142601049` | **YASH JOGANI** | Data Audit & Report Writing |

---

## 📁 Repository File Structure & Descriptions

Below is the directory map matching the dataset files used for Group 5_1 (assigned Trees #201 to #225):

```text
├── README.md                                  # Repository overview and calculation methodology
├── Miyawaki Tree_201 to 225 Data.xlsx        # Raw & cleaned field measurements (Trees 201–225)
└── Generic vs Species Specific Biomass.xlsx   # Allometric comparisons, CO2 rate & Monte Carlo analysis
```

### 1. `Miyawaki Tree_201 to 225 Data.xlsx`
* **Purpose:** Primary field observation database for Group 5_1's assigned 25 trees (Tag IDs #201 to #225).
* **Key Columns:**
  * `Tree_ID`: Unique tag identifier (e.g., T5-01 to T5-25 / Tags 201–225).
  * `Species_Name`: Botanical species identification.
  * `Stem_Count`: Number of active stems recorded per individual.
  * `CBH_cm`: Circumference at breast height ($1.3\text{ m}$) in centimeters.
  * `Height_m`: Total tree height measured via optical clinometer / height stick.
  * `Wood_Density_g_cm3`: Species wood density ($\rho$) sourced from Global Wood Density Database.
  * `Audit_Status`: Notes on valid measurements, corrections, and exclusions (4 trees excluded: dead stems, missing tags, weather restrictions).

### 2. `Generic vs Species Specific Biomass.xlsx`
* **Purpose:** Core analytical workbook containing equations, comparative plots, scaling logic, and Monte Carlo output.
* **Sheet Breakdown:**
  * **Sheet 1 (`Part1_Biomass_Comparison`):** Calculates $\text{AGB}$ using the pantropical Chave et al. (2014) generic model vs. species-specific equations.
    $$\text{DBH} = \frac{\text{CBH}}{\pi}$$
    $$\text{AGB}_{\text{generic}} = 0.0673 \times (\rho \times \text{DBH}^2 \times H)^{0.976}$$
  * **Sheet 2 (`Part2_CO2_Scaling`):** Step-by-step conversion of biomass to carbon ($\times 0.47$) and $\text{CO}_2$ ($\times \frac{44}{12}$), scaling by stand density ($0.75\text{ trees/m}^2$) to $\text{kg CO}_2/\text{ha/year}$, and computing India offset areas ($\text{km}^2$).
  * **Sheet 3 (`Part3_Monte_Carlo_Uncertainty`):** Monte Carlo simulation outputs (1,000 draws/tree) specifying:
    * $\text{DBH} \sim \mathcal{N}(\text{measured}, \sigma = 0.3\text{ cm})$
    * $H \sim \mathcal{N}(\text{measured}, \sigma = 0.8\text{ m})$
    * $\rho \sim \mathcal{U}(\rho_{\min}, \rho_{\max})$
    * Mean biomass and $95\%$ confidence intervals ($2.5^{\text{th}}$ to $97.5^{\text{th}}$ percentiles).

---

## 📊 Summary of Main Results

* **Sample Audit:** 21 valid trees evaluated out of 25 assigned (#201–#225).
* **Sample Occupied Land Area:** $28.0\text{ m}^2$ ($21 \div 0.75\text{ trees/m}^2$).
* **Annual Sequestration Rate:** $\mathbf{39,199.29\text{ kg CO}_2\text{/ha/year}}$ ($39.2\text{ t CO}_2\text{/ha/year}$).
* **India Offset Requirement:** $\mathbf{721,952\text{ km}^2}$ ($\approx 21.96\%$ of India's land area).
* **95% Confidence Bounds:** $30,450$ to $48,120\text{ kg CO}_2\text{/ha/year}$ ($588,100$ to $929,390\text{ km}^2$ required offset area).

---

## 🔗 Key References

1. **Chave, J., et al. (2014).** Improved allometric models to estimate the aboveground biomass of tropical trees. *Global Change Biology*, 20(10), 3177-3190.
2. **Zanne, A. E., et al. (2009).** Global wood density database. *Dryad Digital Repository*.
3. **Friedlingstein, P., et al. (2023).** Global Carbon Budget 2023. *Earth System Science Data*, 15(12), 5301-5369.