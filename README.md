# 🇻🇪 Venezuela Reservoir Analysis

## 📌 Project Overview
This project analyzes Venezuela’s reservoir data to assess:
- Proven vs recoverable reserves
- Production capacity
- Strategic importance of reservoirs
- Historical discovery trends

The project demonstrates a full data workflow:
**CSV → DuckDB → SQL Analysis → Streamlit Dashboard**

---

## 🛠️ Tech Stack
- Python
- Jupyter Notebook (VS Code)
- DuckDB (analytical database)
- SQL
- Streamlit (dashboard)
- Git & GitHub

---

## 📂 Project Structure

reservoir-analysis/
│
├── data/ # Raw CSV dataset
├── notebooks/ # Exploratory & analysis notebooks
├── db/ # Local DuckDB database (ignored by Git)
├── app.py # Streamlit dashboard
├── requirements.txt
├── README.md
└── .gitignore


---

## 🔍 Key Analyses
- Reservoir discovery trends by year/decade
- Total proven reserves by location
- Recoverability ratio (recoverable ÷ proven)
- Production vs reserve sustainability
- Strategic reservoir ranking using a weighted score

---

## 📊 Strategic Scoring Logic
Each reservoir is ranked using:

Strategic Score =
0.4 × Proven Reserves

0.4 × Recoverable Reserves

0.2 × Production Capacity (scaled)


This helps identify high-impact reservoirs for policy and investment decisions.

---

## 🚀 Dashboard Features
- Location-based filtering
- Key KPIs (reserves, production)
- Strategic ranking table
- Clean, reproducible analytics

---

## 🧠 Key Insights
- Venezuela is a mature basin with declining discovery trends
- Reserve concentration creates strategic risk
- Recoverability varies significantly by location
- High production does not always imply high reserves

---

## ▶️ How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py

