"use client";

import {
  ComposedChart,
  Area,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export type ChartPoint = {
  date: string;
  historical?: number;
  forecast?: number;
  range?: [number, number]; // [lower_95, upper_95]
};

type ForecastChartProps = {
  data: ChartPoint[];
};

export default function ForecastChart({ data }: ForecastChartProps) {
  return (
    <div className="w-full h-[420px]">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 11 }}
            interval="preserveStartEnd"
            minTickGap={40}
          />
          <YAxis
            tick={{ fontSize: 11 }}
            label={{
              value: "Thousand MWh",
              angle: -90,
              position: "insideLeft",
              style: { fontSize: 12 },
            }}
          />
          <Tooltip
            formatter={(value: number) => value?.toLocaleString?.() ?? value}
            labelStyle={{ fontWeight: 600 }}
          />
          <Legend />

          {/* 95% confidence band, drawn behind the lines */}
          <Area
            type="monotone"
            dataKey="range"
            name="95% Confidence"
            stroke="none"
            fill="#93c5fd"
            fillOpacity={0.3}
            connectNulls
          />

          <Line
            type="monotone"
            dataKey="historical"
            name="Historical"
            stroke="#1d4ed8"
            strokeWidth={2}
            dot={false}
            connectNulls
          />

          <Line
            type="monotone"
            dataKey="forecast"
            name="Forecast"
            stroke="#dc2626"
            strokeWidth={2}
            strokeDasharray="5 4"
            dot={false}
            connectNulls
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}