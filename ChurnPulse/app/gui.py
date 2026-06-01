import streamlit as st
import requests

# Set page style
st.set_page_config(page_title="ChurnPulse Dashboard", layout="centered")

st.title("📊 ChurnPulse - Customer Health Dashboard")
st.write("Adjust customer metrics below to check real-time risk evaluation from the ML API backend.")

# 1. Setup the interactive input form
st.subheader("👤 Customer Profile")

age = st.slider("Age", min_value=18, max_value=100, value=24, step=1)
monthly_spend = st.slider("Monthly Spend ($)", min_value=10.0, max_value=300.0, value=89.50, step=0.5)
tenure_months = st.slider("Account Tenure (Months)", min_value=0, max_value=72, value=2, step=1)

st.write("---")

# 2. Trigger API calculation on button click
if st.button("Run Health Check Analysis", type="primary"):
    
    # Define the exact FastAPI endpoint URL
    API_URL = "http://127.0.0.1:8000/predict"
    
    # Construct the JSON payload required by your FastAPI input schema
    payload = {
        "age": age,
        "monthly_spend": monthly_spend,
        "tenure_months": tenure_months
    }
    
    try:
        # Send background POST request to the local FastAPI server
        with st.spinner("Querying predictive microservice..."):
            response = requests.post(API_URL, json=payload)
            
        if response.status_code == 200:
            result = response.json()
            
            # Extract data from backend response
            prediction = result["is_predicted_to_churn"]
            probability = result["churn_probability_score"]
            
            # 3. Render clean user feedback cards based on results
            st.subheader("🎯 Risk Assessment Results")
            
            if prediction == 1:
                st.error(f"⚠️ **High Churn Risk Detected!**")
                st.write(f"This customer exhibits behavioral patterns consistent with leaving the service.")
            else:
                st.success(f"✅ **Low Churn Risk / Stable Customer**")
                st.write(f"This customer exhibits strong engagement traits and is highly likely to stay.")
                
            # Display metrics gauge info
            st.metric(label="Calculated Churn Probability", value=f"{round(probability * 100, 1)}%")
            
            # Technical Debug Drawer for GitHub presentation value
            with st.expander("🛠️ Developer Info (API Payload Details)"):
                st.write("**Sent JSON Payload:**")
                st.json(payload)
                st.write("**Received JSON Response:**")
                st.json(result)
                
        else:
            st.error(f"Backend API returned an error code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("❌ **Connection Error:** Could not connect to the FastAPI backend. Make sure your FastAPI server is actively running on port 8000!")