# Trends in CO₂ Emissions and Temperature Variability in the Americas

This project analyzes the temporal trends in CO₂ emissions and temperature variability across North and South America. It highlights key contributors, regional differences, and the relationship between emissions and temperature changes using data from **Our World in Data**.

---

## Table of Contents
- [Introduction](#introduction)
- [Data Sources](#data-sources)
- [Methodology](#methodology)
- [Key Findings](#key-findings)
- [Setup](#setup)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

---

## Introduction

Over the past decades, CO₂ emissions and regional temperatures in North and South America have undergone significant changes. This project aims to provide insights into these trends, with a focus on:
- CO₂ emissions trends by region and key contributors
- Temperature changes and variability
- Correlations between emissions and temperature trends

---

## Data Sources

This project utilizes two datasets sourced from **Our World in Data**:

1. **Monthly Average Surface Temperatures (1960–Present)**  
   - Measures global temperatures across land, sea, and inland surfaces.  
   - URL: [Monthly Average Surface Temperatures](https://ourworldindata.org/grapher/monthly-average-surface-temperatures-by-year)

2. **Annual CO₂ Emissions (1750–2023)**  
   - Tracks emissions from fossil fuels and industrial processes.  
   - URL: [Annual CO₂ Emissions](https://ourworldindata.org/grapher/annual-co-emissions-by-region)

Both datasets are licensed under the Creative Commons BY license.

---

## Methodology

The analysis pipeline includes:

1. **Data Preparation**  
   - Cleaning, transforming, and filtering datasets for the Americas.  
   - Standardizing temperature data and aligning it with emissions data.

2. **Visualization**  
   - Trends visualized using linear and polynomial regressions.  
   - Regional comparisons of CO₂ emissions and temperature variability.

3. **Statistical Analysis**  
   - Regression models used to quantify relationships.  
   - Metrics include slopes, R-squared values, and p-values.

---

## Key Findings

### North America
- The United States is the largest CO₂ emitter, with emissions peaking in 2007.  
- Strong correlation between emissions and rising temperatures.

### South America
- Brazil leads emissions due to deforestation and industrialization.  
- A slower but significant warming trend compared to North America.

### Overall
- Both regions show a strong positive correlation between CO₂ emissions and temperature increases, emphasizing the global warming impact.

---

## Setup

### Prerequisites
- Python 3.8+  
- Jupyter Notebook (optional)  
- Required libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/co2-temperature-trends.git
   ````

2. Navigate to the project directory:
	```bash
	cd co2-temperature-trends
	```

3.	Install dependencies:
	```bash
	pip install -r requirements.txt
	````

### Usage

1. Run the Analysis:

	Open analysis.ipynb in Jupyter Notebook or execute the main script:

```bash
python analysis.py
```

2. View Results

	Results are saved as plots in the output/ folder.

3. Explore Data

	The cleaned datasets are located in the data/ folder for further analysis.

### License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software in accordance with the terms of the license.

The datasets used in this project are sourced from Our World in Data and are licensed under the Creative Commons BY license. Please ensure proper attribution when using these datasets in your own work.

For more details, see the LICENSE file included in the repository.

### Contact

For questions or collaboration, feel free to reach out:

- **Author**: Florian Merlau  
- **Email**: [Florian.Merlau@fau.de](mailto:Florian.Merlau@fau.de)