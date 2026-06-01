import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def build_and_save_model():
    # Synthetic behavioral tracking data: [Age, MonthlySpend, AccountTenureMonths]
    data = {
        'Age': [23, 45, 31, 54, 22, 38, 41, 20],
        'MonthlySpend': [45.5, 110.0, 65.0, 150.2, 89.0, 40.0, 95.5, 115.0],
        'TenureMonths': [2, 24, 11, 36, 1, 18, 14, 3],
        'Churn': [1, 0, 0, 0, 1, 0, 0, 1] # 1 = Left Company, 0 = Active Customer
    }
    df = pd.DataFrame(data)
    
    X = df[['Age', 'MonthlySpend', 'TenureMonths']]
    y = df['Churn']
    
    # Train the machine learning classifier
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Create target deployment folder structure if missing
    os.makedirs("app", exist_ok=True)
    joblib.dump(model, "app/churn_model.pkl")
    print("Production pipeline finalized. Saved binary artifact to app/churn_model.pkl")

if __name__ == "__main__":
    build_and_save_model()