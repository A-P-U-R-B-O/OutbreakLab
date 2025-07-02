# OutbreakLab Architecture

This document describes the advanced architecture of **OutbreakLab**—an interactive platform for simulating, analyzing, and visualizing infectious disease outbreaks using compartmental models (SIR, SEIR, etc.). The design is modular, extensible, and ready for both research and educational deployments.

---

## 1. High-Level Overview

```
┌────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│ Web/App UI │──►│ Controller/UI │──►│ Simulation   │──►│ Visualization│
└────────────┘    └──────────────┘    │  Engine     │    │   Engine    │
                                      └─────────────┘    └─────────────┘
                                             ▲
                                             │
                                      ┌────────────┐
                                      │   Utils &  │
                                      │   Config   │
                                      └────────────┘
```

- **Web/App UI**: Streamlit (or web framework) for user input and result display.
- **Controller/UI Logic**: Orchestrates parameter validation, simulation runs, and visualization calls.
- **Simulation Engine**: Implements SIR, SEIR, and future models (deterministic, stochastic, etc.).
- **Visualization Engine**: Generates plots and summary metrics.
- **Utils & Config**: Parameter validation, conversion, and app-wide settings.

---

## 2. Directory & Module Structure

```
project-root/
│
├── src/
│   ├── app.py             # Main Streamlit app entry point
│   ├── sir_model.py       # SIR/SEIR simulation logic
│   ├── visualization.py   # Plotting and visualization helpers
│   ├── utils.py           # Utility functions (validation, type conversion)
│   ├── config.py          # Default config and constants
│   └── custom.css         # (If not in assets/) Custom style overrides
│
├── assets/
│   ├── custom.css         # Custom CSS for Streamlit/web UI
│   └── example_data.csv   # Example input data for upload/demo
│
├── tests/
│   ├── __init__.py
│   ├── test_sir_model.py
│   ├── test_utils.py
│   └── test_visualization.py
│
└── ARCHITECTURE.md        # (this file)
```

---

## 3. Module Responsibilities

### src/app.py
- Handles UI logic: loads CSS, receives user input, parameter selection, file upload.
- Calls simulation functions and displays results.
- Handles error messages and guides user workflow.

### src/sir_model.py
- Implements core algorithms (deterministic/stochastic SIR, SEIR, etc.).
- Exposes functions for model runs and epidemic metric calculations.
- Designed to be extensible for future models (e.g., SIRD, SEIRS).

### src/visualization.py
- Provides plotting functions (leveraging matplotlib or Plotly).
- Exposes functions for SIR, SEIR, and summary metric visualizations.
- Designed for easy Streamlit and Jupyter integration.

### src/utils.py
- Parameter validation, type conversion, clamping, and helpers.
- Ensures all modules receive safe, well-typed input.

### src/config.py
- Centralizes default values, labels, and app metadata.
- Allows easy override for custom scenarios or deployments.

### assets/custom.css
- Provides a modern, appealing look for the UI.
- Customizes Streamlit widgets, plots, and tables.

### assets/example_data.csv
- Example dataset for demo and testing.
- Useful for users to understand required CSV format and for QA.

---

## 4. Data & Control Flow

1. **User Input**:  
   Via UI controls or CSV file upload. Parameters validated by `utils.py`.

2. **Simulation Run**:  
   UI calls the selected model in `sir_model.py` with user parameters.  
   Results (lists of S, I, R, etc.) returned.

3. **Visualization**:  
   Results passed to `visualization.py` to generate plots and summary metrics.

4. **Display & Export**:  
   UI displays plots and metrics.  
   User can download results or plots.

5. **Testing**:  
   Automated with `pytest` using files in `tests/`.

---

## 5. Extensibility & Customization

- **Adding Models**:  
  Add new model functions to `sir_model.py`.  
  Update `app.py` and `visualization.py` to recognize and plot new compartments.

- **Custom UI**:  
  Modify or extend controls in `app.py` and styles in `custom.css`.

- **New Data Types**:  
  Update `utils.py` and `visualization.py` to support new input/output formats.

---

## 6. Advanced Features (Planned/Future)

- **Multiple Model Comparison**
- **Parameter Sensitivity Analysis**
- **Interactive Timeline/Animation**
- **Batch Processing/Scenario Analysis**
- **Export to Multiple Formats (CSV, PNG, PDF)**
- **Authentication & User Profiles**

---

## 7. Deployment

- **Local:**  
  Run `streamlit run src/app.py`
- **Cloud:**  
  Deploy on Streamlit Cloud, Heroku, or custom Docker image.

---

## 8. Example Execution Path

1. User uploads a CSV or enters parameters.
2. Parameters validated (`utils.py`).
3. Simulation selected and run (`sir_model.py`).
4. Results visualized (`visualization.py`), metrics displayed.
5. User downloads output or tries new scenario.

---

## 9. Testing Philosophy

- Each major module (`sir_model.py`, `utils.py`, `visualization.py`) has dedicated tests.
- Example data used for regression testing.
- CI setup recommended (GitHub Actions, etc.).

---

## 10. Diagram: Component Interaction

```
[User] 
   │
   ▼
[Streamlit UI (app.py)] 
   │
   ├──> [utils.py: validate input] 
   │
   └──> [sir_model.py: run simulation]
           │
           ▼
   [visualization.py: plot & metrics]
           │
           ▼
   [UI: display/download]
```

---

**OutbreakLab is designed for clarity, flexibility, and scientific rigor. Contributions are welcome!**
