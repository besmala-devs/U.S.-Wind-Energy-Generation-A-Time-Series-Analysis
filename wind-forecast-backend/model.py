"""
Ports the R model:
    arima(log_train, order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))

to Python's statsmodels SARIMAX. Same orders, same seasonal period, same
log-transform + back-transform logic as the notebook.
"""
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

MODEL_PATH = "wind_model.pkl"


def fit_model(train: pd.Series):
    """Fit SARIMA(0,1,1)(0,1,1)[12] on the log-transformed training series."""
    log_train = np.log(train)

    model = SARIMAX(
        log_train,
        order=(0, 1, 1),
        seasonal_order=(0, 1, 1, 12),
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    fitted = model.fit(disp=False)
    return fitted


def save_model(fitted, path: str = MODEL_PATH):
    fitted.save(path)


def load_model(path: str = MODEL_PATH):
    from statsmodels.tsa.statespace.sarimax import SARIMAXResults
    return SARIMAXResults.load(path)


def forecast(fitted, steps: int, start_date: str):
    """
    Returns forecast mean + 95% CI, back-transformed from log scale.
    Matches the R script's back-transform:
        fc_mean = exp(pred + 0.5 * var)   # log-normal correction
        fc_lo95 = exp(pred - 1.96 * se)
        fc_hi95 = exp(pred + 1.96 * se)
    """
    result = fitted.get_forecast(steps=steps)
    pred_log = result.predicted_mean
    se_log = result.se_mean
    var_log = se_log ** 2

    fc_mean = np.exp(pred_log + 0.5 * var_log)
    fc_lo95 = np.exp(pred_log - 1.96 * se_log)
    fc_hi95 = np.exp(pred_log + 1.96 * se_log)

    idx = pd.date_range(start=start_date, periods=steps, freq="MS")
    return pd.DataFrame({
        "forecast": fc_mean.values,
        "lower_95": fc_lo95.values,
        "upper_95": fc_hi95.values,
    }, index=idx)


def evaluate(fc_2025: pd.Series, actual_test: pd.Series):
    """RMSE, MAE, MAPE — same formulas as the R script."""
    rmse = np.sqrt(np.mean((fc_2025 - actual_test) ** 2))
    mae = np.mean(np.abs(fc_2025 - actual_test))
    mape = np.mean(np.abs((fc_2025 - actual_test) / actual_test)) * 100
    return {"RMSE": round(rmse, 2), "MAE": round(mae, 2), "MAPE": round(mape, 2)}