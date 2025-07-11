---
title: 'OutbreakLab: An Interactive Platform for Infectious Disease Outbreak Simulation and Visualization'
tags:
  - epidemic modeling
  - streamlit
  - simulation
  - Python
  - SEIR
  - SIR
  - SIRV
  - SEIRV
authors:
  - name: Tamzid Ahmed Apurbo
    orcid: 0009-0002-2518-0928
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 2025-07-11
bibliography: paper.bib
---

## Summary

OutbreakLab is a modern, interactive web application designed to simulate, analyze, and visualize infectious disease outbreaks using compartmental models such as SIR, SEIR, SIRV and SEIRV. Developed in Python with Streamlit, it targets educators, researchers, and students seeking an accessible tool for understanding epidemic dynamics and exploring intervention strategies.

## Statement of Need

Mathematical modeling of infectious diseases is pivotal for both research and education. However, many existing tools are either command-line based, lack interactivity, or are not easily extensible. OutbreakLab addresses these gaps by providing:

- An intuitive web-based UI requiring no programming background  
- Real-time parameter adjustment and visualization  
- Support for both deterministic and stochastic models  
- Uploading of custom or real-world data for scenario analysis  
- Exportable results for reports and further analysis  

OutbreakLab makes epidemic modeling accessible and interactive for the broader scientific and educational community, based on classical frameworks such as SIR and SEIR [@kermack1927contribution].

## Features

- **Model Selection**: SIR,SEIR, SIRV, SEIRV with an extensible framework for more models  
- **Interactive Parameters**: Adjust population size, infection/recovery rates, and other model parameters live  
- **Stochastic & Deterministic Modes**: Explore variability in outbreak outcomes  
- **Data Upload**: Initialize simulations with custom or empirical data via CSV  
- **Modern Visualization**: Interactive plots and metric dashboards  
- **Export Options**: Download results and figures  
- **Customizable UI**: Easily adaptable via CSS  
- **Robust Input Validation**: Prevents nonsensical simulation settings  

## Implementation

OutbreakLab’s architecture is modular and well-documented:

- **Web Application**: Built with Streamlit for rapid UI development and deployment  
- **Simulation Engines**: SIR/SEIR/SIRV/SEIRV models implemented in Python, supporting both deterministic and random processes  
- **Visualization**: Uses Matplotlib for plotting, integrated into the Streamlit dashboard  
- **Utilities**: Data validation, conversion, and configuration modules facilitate reliable and extensible code  
- **Testing**: Comprehensive unit tests ensure correctness and maintainability  

## Usage

### Installation

```bash
git clone https://github.com/A-P-U-R-B-O/OutbreakLab.git
cd OutbreakLab
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run src/app.py
```

Then open `http://localhost:8501` in your web browser.

## Example Data

An example CSV file (`assets/example_data.csv`) is provided for demonstration and as a template for user data.

## Extensibility

- **Adding Models**: Extend `src/sir_model.py` and update the UI in `src/app.py`  
- **Styling**: Customize via `assets/custom.css`  
- **Metrics & Plots**: Modify or add new visualizations in `src/visualization.py`  

## Quality Assurance

- Unit tests are provided for core logic in the `tests/` directory  
- Continuous integration is supported via `pytest`  

## References

The code for OutbreakLab is openly available and archived on Zenodo [@apurbo_outbreaklab_2025].  
This work builds upon foundational epidemic modeling frameworks introduced by [@kermack1927contribution].
