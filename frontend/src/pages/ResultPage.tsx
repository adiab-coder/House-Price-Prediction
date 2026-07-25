import { useLocation, useNavigate } from "react-router-dom";

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();

  // فحص كل الأحتمالات للـ State
  const price = location.state?.predictedPrice ?? location.state?.prediction ?? location.state?.result;

  if (price === undefined || price === null) {
    return (
      <div className="result-container">
        <h2>No prediction found. Please fill out the form first.</h2>
        <button onClick={() => navigate("/")}>Back to form</button>
      </div>
    );
  }

  return (
    <div className="result-container">
      <h2>Estimated House Price</h2>
      <p className="price-display">
        {typeof price === "number" 
          ? `$${price.toLocaleString()}` 
          : JSON.stringify(price)}
      </p>
      <button onClick={() => navigate("/")}>Predict Another</button>
    </div>
  );
}