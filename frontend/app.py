import streamlit as st
import requests
import time
time.sleep(5)

st.set_page_config(page_title="Employee Retention Predictor", layout="wide")

st.title("💼 Employee Retention Prediction System")
st.markdown("Enter employee details below to predict attrition risk")

# ---------------- INPUT FIELDS ---------------- #

col1, col2, col3 = st.columns(3)

with col1:
    Age = st.number_input("Age", 18, 60, 30)

    BusinessTravel = st.selectbox("Business Travel", [0, 1, 2])

    DailyRate = st.number_input("Daily Rate", 100, 2000, 800)

    department_map = {
        "Human Resources": 0,
        "Research & Development": 1,
        "Sales": 2
    }
    Department = department_map[st.selectbox("Department", list(department_map.keys()))]

    DistanceFromHome = st.number_input("Distance From Home", 1, 50, 10)

    Education = st.selectbox("Education", [1, 2, 3, 4, 5])

    EducationField = st.selectbox("Education Field", [0, 1, 2, 3, 4, 5])

with col2:
    EnvironmentSatisfaction = st.selectbox("Environment Satisfaction", [1, 2, 3, 4])

    gender_map = {"Female": 0, "Male": 1}
    Gender = gender_map[st.selectbox("Gender", list(gender_map.keys()))]

    HourlyRate = st.number_input("Hourly Rate", 30, 100, 60)

    JobInvolvement = st.selectbox("Job Involvement", [1, 2, 3, 4])

    JobLevel = st.selectbox("Job Level", [1, 2, 3, 4, 5])

    jobrole_map = {
        "Healthcare Representative": 0,
        "Human Resources": 1,
        "Laboratory Technician": 2,
        "Manager": 3,
        "Manufacturing Director": 4,
        "Research Director": 5,
        "Research Scientist": 6,
        "Sales Executive": 7,
        "Sales Representative": 8
    }
    JobRole = jobrole_map[st.selectbox("Job Role", list(jobrole_map.keys()))]

    JobSatisfaction = st.selectbox("Job Satisfaction", [1, 2, 3, 4])

with col3:
    marital_map = {
        "Divorced": 0,
        "Married": 1,
        "Single": 2
    }
    MaritalStatus = marital_map[st.selectbox("Marital Status", list(marital_map.keys()))]

    MonthlyIncome = st.number_input("Monthly Income", 1000, 25000, 5000)

    MonthlyRate = st.number_input("Monthly Rate", 2000, 30000, 15000)

    NumCompaniesWorked = st.number_input("Companies Worked", 0, 10, 2)

    overtime_map = {"No": 0, "Yes": 1}
    OverTime = overtime_map[st.selectbox("OverTime", list(overtime_map.keys()))]

    PercentSalaryHike = st.number_input("Salary Hike %", 10, 25, 12)

    PerformanceRating = st.selectbox("Performance Rating", [3, 4])

    RelationshipSatisfaction = st.selectbox("Relationship Satisfaction", [1, 2, 3, 4])

    StockOptionLevel = st.selectbox("Stock Option Level", [0, 1, 2, 3])

# More inputs
col4, col5 = st.columns(2)

with col4:
    TotalWorkingYears = st.number_input("Total Working Years", 0, 40, 10)

    TrainingTimesLastYear = st.number_input("Training Times Last Year", 0, 10, 2)

    WorkLifeBalance = st.selectbox("Work Life Balance", [1, 2, 3, 4])

with col5:
    YearsAtCompany = st.number_input("Years At Company", 0, 40, 5)

    YearsInCurrentRole = st.number_input("Years In Current Role", 0, 20, 3)

    YearsSinceLastPromotion = st.number_input("Years Since Last Promotion", 0, 15, 1)

    YearsWithCurrManager = st.number_input("Years With Current Manager", 0, 20, 3)

# ---------------- PREDICTION ---------------- #

if st.button("🔍 Predict"):
    data = {
        "Age": Age,
        "BusinessTravel": BusinessTravel,
        "DailyRate": DailyRate,
        "Department": Department,
        "DistanceFromHome": DistanceFromHome,
        "Education": Education,
        "EducationField": EducationField,
        "EnvironmentSatisfaction": EnvironmentSatisfaction,
        "Gender": Gender,
        "HourlyRate": HourlyRate,
        "JobInvolvement": JobInvolvement,
        "JobLevel": JobLevel,
        "JobRole": JobRole,
        "JobSatisfaction": JobSatisfaction,
        "MaritalStatus": MaritalStatus,
        "MonthlyIncome": MonthlyIncome,
        "MonthlyRate": MonthlyRate,
        "NumCompaniesWorked": NumCompaniesWorked,
        "OverTime": OverTime,
        "PercentSalaryHike": PercentSalaryHike,
        "PerformanceRating": PerformanceRating,
        "RelationshipSatisfaction": RelationshipSatisfaction,
        "StockOptionLevel": StockOptionLevel,
        "TotalWorkingYears": TotalWorkingYears,
        "TrainingTimesLastYear": TrainingTimesLastYear,
        "WorkLifeBalance": WorkLifeBalance,
        "YearsAtCompany": YearsAtCompany,
        "YearsInCurrentRole": YearsInCurrentRole,
        "YearsSinceLastPromotion": YearsSinceLastPromotion,
        "YearsWithCurrManager": YearsWithCurrManager
    }

    try:
        response = requests.post(
            "http://backend:8000/predict",
            json=data,
            timeout=5
        )

        result = response.json()

        # ✅ HANDLE ERROR FROM BACKEND
        if "error" in result:
            st.error(f"❌ Backend Error: {result['error']}")

        else:
            prediction = result["prediction"]
            probability = result["probability_of_leaving"]

            # ✅ SHOW RESULT NICELY
            if prediction == 1:
                st.error(f"⚠️ Employee likely to leave (Probability: {probability:.2f})")
            else:
                st.success(f"✅ Employee likely to stay (Probability: {probability:.2f})")

            # OPTIONAL DEBUG INFO
            st.write("🔍 Raw Response:", result)

    except requests.exceptions.ConnectionError:
        st.error("🚨 Backend not running or not reachable")

    except requests.exceptions.Timeout:
        st.error("⏳ Backend is taking too long. Try again.")

    except Exception as e:
        st.error(f"Error: {e}") 