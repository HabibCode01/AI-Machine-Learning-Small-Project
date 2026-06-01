from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import numpy as np
import os

app = FastAPI(title="ChurnPulse Predictive API", description="Production microservice for tracking customer health scores.")

# Safely load the relative model location context
model_path = os.path.join(os.path.dirname(__file__), "churn_model.pkl")
model = joblib.load(model_path)

# Enforce crisp API body request parameters and bounds
class CustomerFeatures(BaseModel):
    age: int = Field(..., example=24)
    monthly_spend: float = Field(..., example=89.50)
    tenure_months: int = Field(..., example=2)

@app.post("/predict")
def predict_churn(customer: CustomerFeatures):
    # Map raw JSON request inputs into structured array form
    input_features = np.array([[customer.age, customer.monthly_spend, customer.tenure_months]])
    
    prediction = int(model.predict(input_features)[0])
    probability = float(model.predict_proba(input_features)[0][1])
    
    return {
        "is_predicted_to_churn": prediction,
        "churn_probability_score": round(probability, 3)
    }