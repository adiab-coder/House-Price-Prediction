import { useState, FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { predictPrice } from "../api/predictionClient";
import type { PredictionRequest } from "../types/prediction";
import locations from "../locations.json";

const FURNISHING_OPTIONS = ["Furnished", "Semi-Furnished", "Unfurnished"] as const;
const TRANSACTION_OPTIONS = ["New Property", "Resale"] as const;
const OWNERSHIP_OPTIONS = ["Freehold", "Leasehold", "Co-operative Society", "Power Of Attorney"];
const FACING_OPTIONS = ["East", "West", "North", "South", "North - East", "North - West", "South - East", "South -West"];

export default function PredictionForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState<PredictionRequest>({
    location: locations[0] ?? "other",
    area_sqft: 0,
    floor_num: 0,
    bathroom_num: 1,
    balcony_num: 0,
    car_parking_num: 0,
    furnishing: "Semi-Furnished",
    transaction: "Resale",
    ownership: "Freehold",
    facing: "East",
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  function update<K extends keyof PredictionRequest>(key: K, value: PredictionRequest[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

 async function handleSubmit(e: FormEvent) {
  e.preventDefault();
  setError(null);

  if (!form.location) {
    setError("Please select a location.");
    return;
  }
  if (form.area_sqft <= 0) {
    setError("Area must be greater than 0.");
    return;
  }
  if (form.bathroom_num < 0 || form.balcony_num < 0 || form.car_parking_num < 0) {
    setError("Counts cannot be negative.");
    return;
  }

  setLoading(true);
  try {
    const result = await predictPrice(form);
    console.log("API Response:", result); // طباعة الرد للتأكد في الـ Console

    // استخراج السعر سواء كان المرجع predicted_price أو price أو القيمة نفسها
    const priceValue = result.predicted_price ?? (result as any).price ?? result;

    navigate("/result", { 
      state: { 
        predictedPrice: priceValue,
        prediction: priceValue,
        result: result
      } 
    });
  } catch (err) {
    setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
  } finally {
    setLoading(false);
  }
}
  return (
    <form onSubmit={handleSubmit} className="prediction-form">
      <label>
        Location
        <select value={form.location} onChange={(e) => update("location", e.target.value)}>
          {locations.map((loc: string) => (
            <option key={loc} value={loc}>{loc}</option>
          ))}
        </select>
      </label>

      <label>
        Area (sqft)
        <input
          type="number"
          min={1}
          value={form.area_sqft}
          onChange={(e) => update("area_sqft", Number(e.target.value))}
          required
        />
      </label>

      <label>
        Floor
        <input
          type="number"
          value={form.floor_num}
          onChange={(e) => update("floor_num", Number(e.target.value))}
          required
        />
      </label>

      <label>
        Bathrooms
        <input
          type="number"
          min={0}
          value={form.bathroom_num}
          onChange={(e) => update("bathroom_num", Number(e.target.value))}
          required
        />
      </label>

      <label>
        Balconies
        <input
          type="number"
          min={0}
          value={form.balcony_num}
          onChange={(e) => update("balcony_num", Number(e.target.value))}
        />
      </label>

      <label>
        Car Parking
        <input
          type="number"
          min={0}
          value={form.car_parking_num}
          onChange={(e) => update("car_parking_num", Number(e.target.value))}
        />
      </label>

      <label>
        Furnishing
        <select value={form.furnishing} onChange={(e) => update("furnishing", e.target.value as PredictionRequest["furnishing"])}>
          {FURNISHING_OPTIONS.map((opt) => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </label>

      <label>
        Transaction
        <select value={form.transaction} onChange={(e) => update("transaction", e.target.value as PredictionRequest["transaction"])}>
          {TRANSACTION_OPTIONS.map((opt) => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </label>

      <label>
        Ownership
        <select value={form.ownership} onChange={(e) => update("ownership", e.target.value)}>
          {OWNERSHIP_OPTIONS.map((opt) => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </label>

      <label>
        Facing
        <select value={form.facing} onChange={(e) => update("facing", e.target.value)}>
          {FACING_OPTIONS.map((opt) => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </label>

      {error && <p className="form-error">{error}</p>}

      <button type="submit" disabled={loading}>
        {loading ? "Predicting..." : "Predict Price"}
      </button>
    </form>
  );
}
