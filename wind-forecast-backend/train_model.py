"""
 python train_model.py
"""
from data_loader import load_wind_series, train_test_split
from model import fit_model, save_model, forecast, evaluate

if __name__ == "__main__":
    series = load_wind_series()
    train, test = train_test_split(series)

    print("Fitting SARIMA(0,1,1)(0,1,1)[12] ...")
    #fitted = fit_model(train)
    #save_model(fitted)
    print("Saved to wind_model.pkl")

    print(fitted.summary())

    # Sanity check against the held-out 2025 data, same as the notebook
    fc = forecast(fitted, steps=24, start_date="2025-01-01")
    fc_2025 = fc["forecast"][:12]
    fc_2025.index = test.index  # align for comparison

    metrics = evaluate(fc_2025, test)
    print("\nEvaluation against 2025 actuals:")
    print(metrics)
    print("(Notebook reported: RMSE 4223.74, MAE 3630.21 , MAPE 10.53%)")
    """
    {'RMSE': np.float64(4088.18), 'MAE': np.float64(3508.65), 'MAPE': np.float64(10.16)}
    """