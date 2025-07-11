# 🦠 OutbreakLab

**OutbreakLab** is an interactive, modern web application for simulating, analyzing, and visualizing infectious disease outbreaks using compartmental models like SIR, SEIR, and SIRV. Designed for education, research, and rapid scenario analysis, OutbreakLab features an appealing UI, flexible input (manual or CSV), stochastic and deterministic modeling, and rich visualizations.

---

## 🚀 Features

- **Model Selection:** SIR, SEIR, SIRV and SEIRV (extensible for more)
- **Interactive Parameters:** Adjust population, rates, durations, and vaccination on the fly
- **CSV Upload:** Start simulations from real or custom data
- **Stochastic & Deterministic Modes:** Compare epidemic randomness vs. average trends
- **Visualization:** Beautiful, modern plots and summary metric dashboards
- **Downloadable Results:** Export data and figures for reports or further analysis
- **Customizable UI:** Stylish, responsive design (see `assets/custom.css`)
- **Robust Validation:** Prevents invalid or nonsensical parameter sets
- **Extensible Codebase:** Easy to add new models, metrics, or UI features

---

## 🏗️ Architecture

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for a detailed overview.  
Main components:
- `src/app.py`: Streamlit app entry point and UI logic
- `src/sir_model.py`: SIR/SEIR/SIRV simulation engines
- `src/visualization.py`: Plotting & metric visualization (supports SIR, SEIR, SIRV)
- `src/utils.py`: Validation, conversion, helpers
- `src/config.py`: App defaults and metadata
- `assets/`: Custom CSS, example data

---

## 🖥️ Quickstart

### 1. Clone & Install

```bash
git clone https://github.com/A-P-U-R-B-O/OutbreakLab.git
cd OutbreakLab
pip install -r requirements.txt
```

### 2. Run the App

```bash
streamlit run src/app.py
```

### 3. Open in Your Browser

Streamlit will open a local server, usually at [http://localhost:8501](http://localhost:8501).

Or try the live app:  
**🌐 [OutbreakLab Demo](https://outbreaklab.streamlit.app/)**

---

## 📁 File Structure

```
OutbreakLab/
├── src/
│   ├── app.py
│   ├── sir_model.py
│   ├── visualization.py
│   ├── utils.py
│   └── config.py
├── assets/
│   ├── custom.css
│   └── example_data.csv
├── tests/
│   ├── test_sir_model.py
│   ├── test_utils.py
│   └── test_visualization.py
├── ARCHITECTURE.md
├── README.md
└── requirements.txt
```

---

## 📊 Example Data

Use `assets/example_data.csv` as a template for uploading your own outbreak data.

---

## 🧪 Testing

Run all unit tests with:

```bash
pytest
```

---

## 🛠️ Customization

- **Add Models:** Extend `sir_model.py` and update UI in `app.py`
- **Style:** Edit `assets/custom.css`
- **Metrics:** Add or modify in `visualization.py`

---

## 📜 License

MIT License (see [LICENSE](LICENSE))

---

## 🤝 Contributions

Contributions are welcome!  
Open an issue or PR for features, models, bugfixes, or improvements.

---

## 🌐 Links

- [GitHub](https://github.com/A-P-U-R-B-O/OutbreakLab)
- Example data: [`assets/example_data.csv`](assets/example_data.csv)
- Architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- **Live App:** [https://outbreaklab.streamlit.app](https://outbreaklab.streamlit.app/)

---

> OutbreakLab: Making epidemic modeling accessible, beautiful, and insightful.
