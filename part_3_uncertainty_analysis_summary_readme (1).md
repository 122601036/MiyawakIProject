# Part 3: Monte Carlo Uncertainty Analysis Summary

## 📊 Methodology & Error Distributions

To quantify uncertainty in generic Chave AGB estimates, a 1,000-draw Monte Carlo simulation per tree was implemented (every stem of all 21 trees perturbed independently; fixed random seed). Uncertainty distributions were specified based on field measurement precision:

* **Diameter at Breast Height ($\text{DBH}$):** Normal distribution $\mathcal{N}(\text{DBH}, \sigma = 0.3\text{ cm})$ reflecting tape alignment error.
* **Height ($H$):** Normal distribution $\mathcal{N}(H, \sigma = 0.8\text{ m})$ accounting for optical clinometer visual obstruction.
* **Wood Density ($\rho$):** Uniform distribution $\mathcal{U}(0.9\rho, 1.1\rho)$, i.e., $\pm 10\%$ around the species value in the group sheet, as the sheet holds a single $\rho$ per species [2].

---

## 📈 Figure 2 Summary

> **Figure 2:** Mean Biomass with $95\%$ Confidence Intervals ($2.5\text{th}$ to $97.5\text{th}$ Percentiles) from 1,000 Monte Carlo Draws
> 
> * **Y-Axis:** Mean AGB ($\text{kg}$) $[0, 10, 20]$
> * **X-Axis (Tree IDs):** `201`, `202`, `203`, `204`, `205`, `207`, `210`, `211`, `212`, `213`, `214`, `215`, `216`, `218`, `219`, `220`, `221`, `222`, `223`, `224`, `225`

---

## 🔍 Uncertainty Driver Analysis

The smallest trees show the widest $95\%$ intervals (trees `207`, `224`, and `201`: $\pm 131\%$ to $\pm 110\%$ of the mean), because fixed height and diameter errors are large relative to stems only about $2\text{ m}$ tall; the largest trees (`215` and `210`) are tightest ($\pm 30\%$ to $\pm 32\%$). A one-at-a-time variance analysis attributes:

* **Height Error:** $66\%$ of total variance
* **$\text{DBH}$ Error:** $25\%$ of total variance
* **Wood Density Error:** $9\%$ of total variance

### 🎯 Key Results & National Offset Propagation

* **Total Stand AGB:** $90.4\text{ kg}$ ($95\%$ interval: $79.6\text{–}101.4\text{ kg}$)
* **Annual Sequestration Rate:** $9,795\text{ to }12,487\text{ kg CO}_2/\text{ha/year}$
* **Required National Offset Area:** $2,266,320\text{ to }2,889,170\text{ km}^2$ ($68.9\%\text{ to }87.9\%$ of India's land area)