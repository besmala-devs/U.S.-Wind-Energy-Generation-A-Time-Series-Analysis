# U.S. Wind Energy Generation: Time Series Analysis & Forecasting

## 📊 Project Overview
This project analyzes and forecasts monthly net wind energy generation in the U.S. (thousand MWh) using data from the **U.S. Energy Information Administration (EIA)** spanning 2001 to 2025. 

Using a rigorous three-phase methodology—**Identification, Estimation, and Forecasting**—this project successfully models the exponential growth and inherent seasonality of renewable energy production.

## 🛠️ Technical Methodology
I implemented a **SARIMA** (Seasonal Auto-Regressive Integrated Moving Average) approach to handle the non-stationary nature of the energy data:
* **Preprocessing:** Log transformation and differencing to stabilize variance and remove trends.
* **Model Selection:** A **SARIMA(0,1,1)(0,1,1)[12]** model was selected based on the Bayesian Information Criterion (BIC).
* **Validation:** Residual diagnostics confirmed white noise behavior, and the model achieved a **MAPE (Mean Absolute Percentage Error) of 10.53%**.

## 🚀 Key Insights
* **Seasonal Peaks:** Analysis reveals that wind generation consistently peaks in **February, March, and April**, with a significant drop during summer months.
* **Growth Trends:** The model captures the dramatic shift in the U.S. energy landscape over the last two decades.
* **Forecasting:** Includes a 24-month ahead forecast for grid stability and investment planning insights.

## 📂 Repository Structure
* `analysis_notebook.ipynb`: Full R/Python implementation including data visualization and SARIMA modeling.
* `Net_generation_wind_all_sectors_monthly.csv`: The primary dataset (2001–2025).
* `README.md`: Project documentation.

