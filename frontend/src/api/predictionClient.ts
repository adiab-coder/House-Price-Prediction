import type { PredictionRequest, PredictionResponse } from "../types/prediction";

// استخدام رابط الباك إند المباشر على Vercel مع الـ Fallback
const BASE_URL = (import.meta.env.VITE_API_BASE_URL as string) || "https://house-price-prediction-l83b.vercel.app";

export async function predictPrice(
  payload: PredictionRequest
): Promise<PredictionResponse> {
  const response = await fetch(`${BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Prediction request failed (${response.status}): ${detail}`);
  }

  return response.json();
}
