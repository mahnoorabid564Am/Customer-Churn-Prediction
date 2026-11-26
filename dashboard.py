
import streamlit as st
import pandas as pd


# Load and prepare dataset
@st.cache_data
def load_data():

    data = pd.read_csv(
        "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    )

    data["TotalCharges"] = pd.to_numeric(
        data["TotalCharges"],
        errors="coerce"
    )

    data = data.dropna(subset=["TotalCharges"])

    return data


# --------------------------------
# Dashboard Page
# --------------------------------

def show_dashboard():

    data = load_data()

    st.title("Customer Churn Dashboard")
    st.write("Overview of customer retention and churn.")

    total_customers = len(data)

    churned_customers = (data["Churn"] == "Yes").sum()

    retained_customers = (data["Churn"] == "No").sum()

    churn_rate = (churned_customers / total_customers) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total_customers)
    col2.metric("Churned Customers", churned_customers)
    col3.metric("Retained Customers", retained_customers)
    col4.metric("Churn Rate", f"{churn_rate:.2f}%")

    st.subheader("Customer Records")

    churn_filter = st.selectbox(
        "Filter customers by churn status",
        ["All", "Yes", "No"]
    )

    if churn_filter == "All":
        filtered_data = data
    else:
        filtered_data = data[data["Churn"] == churn_filter]

    st.dataframe(filtered_data, use_container_width=True)


# --------------------------------
# Analytics Page
# --------------------------------

def show_analytics():

    data = load_data()

    st.title("Customer Churn Analytics")

    # Overall churn distribution
    st.subheader("Customer Churn Distribution")

    churn_counts = data["Churn"].value_counts()

    st.bar_chart(churn_counts)

    # Churn by contract
    st.subheader("Churn by Contract Type")

    contract_churn = pd.crosstab(
        data["Contract"],
        data["Churn"]
    )

    st.bar_chart(contract_churn)

    # Churn percentage by contract
    st.subheader("Churn Rate by Contract Type")

    contract_churn_rate = (
        contract_churn["Yes"] / contract_churn.sum(axis=1)
    ) * 100

    st.bar_chart(contract_churn_rate)

    # Churn by payment method
    st.subheader("Churn by Payment Method")

    payment_churn = pd.crosstab(
        data["PaymentMethod"],
        data["Churn"]
    )

    st.write(
        payment_churn["Yes"].sort_values(ascending=False)
    )

    st.bar_chart(payment_churn)

    # Average tenure
    st.subheader("Average Customer Tenure")

    tenure_data = data.groupby("Churn")["tenure"].mean()

    st.bar_chart(tenure_data)


# --------------------------------
# Prediction Page
# --------------------------------

def show_prediction():

    st.title("Customer Churn Prediction")

    st.info(
        "Demonstration only: This is a rule-based example, "
        "not a trained machine learning prediction."
    )

    with st.form("prediction_form"):

        tenure = st.number_input(
            "Customer Tenure (months)",
            min_value=0,
            max_value=72,
            value=12
        )

        contract = st.selectbox(
            "Contract Type",
            ["Month-to-month", "One year", "Two year"]
        )

        monthly_charges = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            value=70.0
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

        predict_button = st.form_submit_button(
            "Demonstrate Churn Risk"
        )

    if predict_button:

        risk_score = 0

        if contract == "Month-to-month":
            risk_score += 40

        if tenure < 12:
            risk_score += 30

        if payment_method == "Electronic check":
            risk_score += 20

        if monthly_charges > 80:
            risk_score += 10

        st.subheader("Demonstration Result")

        st.write(
            f"Illustrative Risk Score: {risk_score}/100"
        )

        if risk_score >= 60:
            st.warning("Illustrative Risk Level: High")

        elif risk_score >= 30:
            st.info("Illustrative Risk Level: Medium")

        else:
            st.success("Illustrative Risk Level: Low")
