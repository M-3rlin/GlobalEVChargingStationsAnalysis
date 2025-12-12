# Global EV Charging Station Analysis

A comprehensive data analysis project aimed at **optimising the global Electric Vehicle (EV) charging network**. This project integrates four key business streams—**Vehicle Economics**, **Pricing Models**, **Availability Analysis**, and **Infrastructure Mapping**—to provide actionable insights for customers and network planners.

## 1. Project Overview

**Core Question:** How can we optimise the EV charging network to balance pricing fairness, station availability, and vehicle efficiency for diverse user groups?

This project analyses real-world charging logs and 2025 market data to answer this question. We have built a centralised dashboard that allows users to:

* **Find Stations:** View charger clusters and stats on an interactive map.
* **Predict Costs:** Estimate session prices based on time, location, and charger type.
* **Check Availability:** Forecast the likelihood of finding a free spot.
* **Compare Vehicles:** Calculate the "Cheapest Mile" running cost for specific car models.

> **Note:** The interactive dashboard code is hosted in a separate repository by Sam. This repository contains this portion of the project: https://github.com/samhsforrest-collab/TEAM-PROJECT-2

---

## 2. Getting Started

Instructions on how to get a copy of the project up and running on a local machine for development and testing purposes.

### Prerequisites

List of software and dependencies required to run the project notebooks and scripts:

* Python (version 3.8 or higher)
* Libraries: `pip install pandas numpy scikit-learn matplotlib seaborn plotly pydeck`
* Jupyter Notebook or VS Code (for running `.ipynb` files)

### Installation

1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/M-3rlin/GlobalEVChargingStationsAnalysis.git](https://github.com/M-3rlin/GlobalEVChargingStationsAnalysis.git)
    ```

2.  **Install packages:**
    ```bash
    pip install -r requirements.txt
    ```
    > **Note:** Ensure you create a `requirements.txt` file if one does not exist.

---

## 3. Key Features & Analysis Streams

Our analysis is divided into four specialised streams, each led by a team member:

### Stream 1: Cars & Economics (Lead: Abdul)
* **Objective:** Analyse vehicle efficiency and running costs.
* **Key Feature:** **"Cheapest Mile Predictor"** - A hybrid model using 2025 spec data and historical user logs to predict the cost-per-km for specific vehicles in specific cities.
* **Visuals:** Efficiency vs. Price scatter plots, Body Type comparisons (SUV vs. Sedan).

### Stream 2: Pricing Models (Lead: Swathi)
* **Objective:** Understand cost drivers and predict session prices.
* **Key Feature:** Random Forest Regression model to estimate charging costs based on charger type (DC Fast vs. Level 2) and time of day.
* **Visuals:** Price distribution box plots, Correlation heatmaps.

### Stream 3: Availability (Lead: Arphaxad)
* **Objective:** Optimise station utilisation.
* **Key Feature:** Temporal analysis identifying peak usage windows (e.g., Weekday Evenings) and "charging deserts."
* **Visuals:** Utilisation heatmaps, Peak time bar charts.

### Stream 4: Mapping (Lead: Raphael)
* **Objective:** Visualise infrastructure gaps.
* **Key Feature:** Interactive geospatial mapping of station density, charger types, and distance-to-city metrics.
* **Visuals:** Clustered map layers, Hover-over station tooltips.

---

## 4. Team Members

This project was a collaborative effort by:

* **Sam** (Dashboard Integration & Team Review)
* **Abdul** (Cars Stream Analysis)
* **Swathi** (Pricing Stream Analysis)
* **Arphaxad** (Availability Analysis)
* **Raphael** (Mapping Analysis)
