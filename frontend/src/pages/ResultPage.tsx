import { useLocation, useNavigate } from "react-router-dom";

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const price = location.state?.predictedPrice;

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
          ? `${price.toLocaleString()} EGP`
          : typeof price === "object" && price.predicted_price
          ? `${Number(price.predicted_price).toLocaleString()} EGP`
          : JSON.stringify(price)}
      </p>
      <button onClick={() => navigate("/")}>Predict Another</button>
    </div>
  );
}