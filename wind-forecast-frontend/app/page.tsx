"use client";

import { useEffect, useState } from "react";
import MonthsSelector from "./components/MonthSelector";
import ForecastChart, { ChartPoint } from "./components/ForecastChart";

const API_BASE = "http://127.0.0.1:8000";

type HistoryResponse = {
  dates: string[];
  values: number[];
};

type PredictResponse = {
  months: number;
  dates: string[];
  forecast: number[];
  lower_95: number[];
  upper_95: number[];
};

export default function Home() {
  const [months, setMonths] = useState(24);
  const [chartData, setChartData] = useState<ChartPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      setError(null);
      try {
        const [historyRes, predictRes] = await Promise.all([
          fetch(`${API_BASE}/history`),
          fetch(`${API_BASE}/predict?months=${months}`),
        ]);

        if (!historyRes.ok || !predictRes.ok) {
          throw new Error("API request failed");
        }

        const history: HistoryResponse = await historyRes.json();
        const predict: PredictResponse = await predictRes.json();

        // Only show the last few years of history so the chart isn't dominated
        // by 25 years of data next to a 1-3 year forecast
        const RECENT_MONTHS = 48;
        const recentDates = history.dates.slice(-RECENT_MONTHS);
        const recentValues = history.values.slice(-RECENT_MONTHS);

        const historyPoints: ChartPoint[] = recentDates.map((date, i) => ({
          date,
          historical: recentValues[i],
        }));

        const forecastPoints: ChartPoint[] = predict.dates.map((date, i) => ({
          date,
          forecast: predict.forecast[i],
          range: [predict.lower_95[i], predict.upper_95[i]],
        }));

        // Bridge point so the forecast line connects to the last historical point
        if (historyPoints.length > 0) {
          const lastHistorical = historyPoints[historyPoints.length - 1];
          forecastPoints.unshift({
            date: lastHistorical.date,
            forecast: lastHistorical.historical,
            range: [lastHistorical.historical!, lastHistorical.historical!],
          });
        }

        setChartData([...historyPoints, ...forecastPoints]);
      } catch (err) {
        setError(
          "Couldn't reach the forecast API. Make sure the FastAPI backend is running on port 8000."
        );
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [months]);

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">
          U.S. Wind Generation Forecast
        </h1>
        <p className="text-gray-500 mb-6">
          SARIMA(0,1,1)(0,1,1)[12] model &middot; monthly net generation, 2001&ndash;2025
        </p>

        <div className="mb-6">
          <MonthsSelector value={months} onChange={setMonths} />
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          {loading && (
            <div className="h-[420px] flex items-center justify-center text-gray-400">
              Loading forecast...
            </div>
          )}
          {error && (
            <div className="h-[420px] flex items-center justify-center text-red-500 text-sm">
              {error}
            </div>
          )}
          {!loading && !error && <ForecastChart data={chartData} />}
        </div>
      </div>
    </main>
  );
}