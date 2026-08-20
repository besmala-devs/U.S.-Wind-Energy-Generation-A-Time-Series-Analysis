"use client";

type MonthsSelectorProps = {
  value: number;
  onChange: (months: number) => void;
};

const OPTIONS = [12, 24, 36];

export default function MonthsSelector({ value, onChange }: MonthsSelectorProps) {
  return (
    <div className="flex gap-2">
      {OPTIONS.map((months) => (
        <button
          key={months}
          onClick={() => onChange(months)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            value === months
              ? "bg-blue-600 text-white"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
        >
          {months} months
        </button>
      ))}
    </div>
  );
}