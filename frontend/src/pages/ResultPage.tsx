import { useLocation, useNavigate } from "react-router-dom";

function formatIndianPrice(amount: number): string {
  if (amount >= 1e7) return `₹ ${(amount / 1e7).toFixed(2)} Cr`;
  if (amount >= 1e5) return `₹ ${(amount / 1e5).toFixed(2)} Lac`;
  return `₹ ${amount.toLocaleString("en-IN")}`;
}

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const predictedPrice = (location.state as { predictedPrice?: number } | null)?.predictedPrice;

  if (predictedPrice === undefined) {
    return (
      <main className="page">
        <p>No prediction found. Please fill out the form first.</p>
        <button onClick={() => navigate("/")}>Back to form</button>
      </main>
    );
  }

  return (
    <main className="page">
      <h1>Estimated Price</h1>
      <p className="predicted-price">{formatIndianPrice(predictedPrice)}</p>
      <button onClick={() => navigate("/")}>Predict another property</button>
    </main>
  );
}
