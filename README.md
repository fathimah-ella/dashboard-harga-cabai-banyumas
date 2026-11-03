# 🌶️ Bird's Eye Chili Price Dashboard, Banyumas

**Live dashboard:** [https://REPLACE-WITH-YOUR-LINK.streamlit.app](https://harga-cabai-rawit-banyumas.streamlit.app/)

Interactive dashboard and supporting code for the ICoCSETI 2026 conference paper:

> *Bird's Eye Chili Price Prediction Using ST-GCN Based on Inter-Market Price Correlation in Banyumas Regency*
> Fathimah Ella Syarif

## About

This repository contains the Streamlit dashboard and the training notebook for our study on bird's eye chili (*cabai rawit*) price prediction across **14 traditional markets in Banyumas Regency, Indonesia**.

We compare a spatio-temporal graph convolutional network (ST-GCN) built on an **inter-market price-correlation graph** against three alternatives: an ST-GCN built on a **distance-based graph**, a **GRU without a graph**, and a **naive persistence** baseline. In our experiments the naive persistence baseline achieved the lowest error (16.71% MAPE vs. 23.03% for the correlation-graph ST-GCN), and we report this result as is. The dashboard lets you explore price patterns and simulate the models on the held-out test period.

> **Note:** the dashboard interface is in Indonesian, because it is designed for local stakeholders (traders, farmers, and the local trade office).

---

## 1. What the dashboard contains

The dashboard has two pages (sidebar menu).

### Home: Price Insights (*Beranda: Insight Harga*)
Answers practical questions about chili prices in the 14 markets:
- **What is the price situation now?** Each market gets a status: Normal, Alert (*Waspada*, price up ≥25% in 30 days), or Critical (*Siaga*, up ≥50%).
- **Which markets are the most and least expensive?** Includes the west-to-east price pattern across the regency.
- **When do prices usually surge?** A list of surge episodes (district-average price up ≥50% within 30 days).
- **Which markets rise first?** An early-warning view showing which markets tend to move before the others follow.
- Every section ends with an **insight** (how many rupiah or percent prices moved) and a **recommendation**.

### Prediction: Model Simulation (*Prediksi: Simulasi Model*)
Compares the four models on the **test set** (target dates 18 Aug – 31 Dec 2025), which was never used during training:
- Choose the **market**, **chili type** (red / green bird's eye chili), **models** (one or several), **forecast start date**, and **number of days ahead** (1–30).
- Output: predicted vs. actual price chart, a per-date table (downloadable as CSV), and MAE / MAPE for each model.
- A "Details for researchers" section gives the full comparison and statistical tests.

> **Note:** this is a simulation on past (test) data, not an official forecast of future prices.

## 2. Models compared

| Model | Short description |
|---|---|
| **Naive persistence** | Predicts that tomorrow's price equals the last known price. The simplest possible baseline. |
| **GRU (no graph)** | A time-series model that learns each market's own price pattern without using relationships between markets. |
| **ST-GCN (distance)** | GRU plus a market graph based on **geographic distance** between markets. |
| **ST-GCN (correlation)** | GRU plus a market graph based on **similarity of price movements** (correlation threshold 0.65 → 85 edges out of 91 market pairs). |

Main setup: 14 markets, 14-day input window (6 features), 30-day forecast horizon, for both red and green bird's eye chili. Final predictions are the average of an ensemble of 5 random seeds.

## 3. Main results (test set)

| Model | MAPE, ensemble | Mean ± std across seeds |
|---|---|---|
| Naive persistence | **16.71%** | n/a |
| GRU (no graph) | 22.39% | 23.00 ± 2.47 |
| ST-GCN (distance) | 22.54% | 23.78 ± 2.65 |
| ST-GCN (correlation) | 23.03% | 24.37 ± 3.36 |

We report these findings as they are: on this dataset, **naive persistence is more accurate** than the graph-based models, and the differences among the GRU-based models are not statistically significant (paired t-test, p = 0.60 for correlation vs. GRU). The reasons and limitations are discussed in the paper. The dashboard lets readers inspect these comparisons themselves.

## 4. Repository structure

```
dashboard-harga-cabai-banyumas/
├── app.py                        # dashboard code (Streamlit)
├── requirements.txt              # libraries for the dashboard
├── requirements-notebook.txt     # extra libraries for the notebook (PyTorch, etc.)
├── README.md                     # this file
├── .gitignore
├── .streamlit/
│   └── config.toml               # light theme
├── data/
│   └── dinperindag_2023-2025_clean.xlsx   # daily prices, 14 markets
├── model_r2/                     # notebook outputs (STEP 15), read by the dashboard
│   ├── pred_m_rp.npy, pred_h_rp.npy              # ST-GCN (correlation) predictions, red / green, in Rupiah
│   ├── pred_jarak_m_rp.npy, pred_jarak_h_rp.npy  # ST-GCN (distance) predictions
│   ├── pred_gru_m_rp.npy, pred_gru_h_rp.npy      # GRU (no graph) predictions
│   ├── pred_persist_m_rp.npy, pred_persist_h_rp.npy  # naive persistence predictions
│   ├── y_m_rp.npy, y_h_rp.npy                    # actual prices
│   ├── daftar_pasar.npy, daftar_tanggal.npy      # market names and dates
│   ├── adj_matrix.npy, info_dashboard.json       # correlation graph and extra info
│   └── model_best.pt, scaler_*.pkl, history_*.npy, best_epoch*.npy, tensor_data.npy
└── notebook/
    └── Prediksi_Cabai_Rawit_GNN.ipynb     # training and evaluation notebook
```

## 5. Run the dashboard locally

Requires Python 3.11 or 3.12.

```bash
# 1. Download this repository (green "Code" button → Download ZIP, then extract)
cd dashboard-harga-cabai-banyumas

# 2. (Recommended) create a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install the libraries
pip install -r requirements.txt

# 4. Run
streamlit run app.py
```

Your browser opens automatically at `http://localhost:8501`.

## 6. Re-run the notebook (optional)

The notebook is only needed to **retrain** the models. The dashboard does not require it.

1. Install PyTorch for your machine (see https://pytorch.org/get-started/locally/).
2. `pip install -r requirements-notebook.txt`
3. Open `notebook/Prediksi_Cabai_Rawit_GNN.ipynb` in Jupyter or VS Code and run the cells from top to bottom.
4. The finished notebook creates the `model_r2/` folder (STEP 15). Copy that folder into this repository to update the dashboard.

Note: the distance-graph ST-GCN is run from a separate notebook, and its predictions are copied into `model_r2/` at STEP 15.

## 7. Data

- **Source:** daily bird's eye chili prices from the Banyumas Regency Department of Industry and Trade (Dinperindag).
- **Coverage:** 14 markets, January 2023 – December 2025, red and green bird's eye chili.
- **Split:** 773 training, 107 validation, and 107 test samples, in chronological order with a 29-sample gap to prevent leakage. Test target dates: 18 Aug – 31 Dec 2025.
- **Missing values:** 5.8% of rows (at the start of some series, all inside the training set) were filled by backward fill. In the test period, 97% of prices are real observations.

## 8. Limitations

- The test period is only about 4.5 months and contains one large price surge (December 2025), so results are sensitive to that period.
- Naive persistence is hard to beat at short horizons, and the graph-based models did not show an advantage on this dataset.
- The dashboard is a simulation on test data, not an operational early-warning system.

## 9. Citation

```
F. E. Syarif, "Bird's Eye Chili Price Prediction Using ST-GCN Based on Inter-Market
Price Correlation in Banyumas Regency," ICoCSETI 2026.
```

## 10. Contact

Fathimah Ella Syarif, Universitas Telkom Purwokerto
Email: faatheellaa@gmail.com
Questions and suggestions are also welcome in the **Issues** tab of this repository.
