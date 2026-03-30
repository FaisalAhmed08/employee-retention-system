import fastapi
import pickle
import numpy as np
import pandas as pd
import mysql.connector
import time

def connect_db():
    while True:
        try:
            conn = mysql.connector.connect(
                host="db",
                user="root",
                password="Faisal.123",
                database="employee_db"
            )
            print("✅ Connected to MySQL")
            return conn
        except Exception as e:
            print("⏳ Waiting for MySQL...", e)
            time.sleep(5)

conn = connect_db()
cursor = conn.cursor()

    
app = fastapi.FastAPI()

# Load model
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# Feature names (IMPORTANT - must match training)
columns = [
    'Age','BusinessTravel','DailyRate','Department','DistanceFromHome',
    'Education','EducationField','EnvironmentSatisfaction','Gender',
    'HourlyRate','JobInvolvement','JobLevel','JobRole','JobSatisfaction',
    'MaritalStatus','MonthlyIncome','MonthlyRate','NumCompaniesWorked',
    'OverTime','PercentSalaryHike','PerformanceRating','RelationshipSatisfaction',
    'StockOptionLevel','TotalWorkingYears','TrainingTimesLastYear',
    'WorkLifeBalance','YearsAtCompany','YearsInCurrentRole',
    'YearsSinceLastPromotion','YearsWithCurrManager'
]

@app.get("/")
def home():
    return {"message": "Employee Retention API Running 🚀"}

@app.post("/predict")
def predict(data: dict):
    try:
        input_df = pd.DataFrame([data], columns=columns)

        scaled = scaler.transform(input_df)

        prediction = model.predict(scaled)[0]
        probability = model.predict_proba(scaled)[0][1]

        # 🔥 INSERT INTO DATABASE
        query = """
        INSERT INTO predictions (Age, Department, JobRole, MonthlyIncome, OverTime, prediction, probability)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data["Age"],
            data["Department"],
            data["JobRole"],
            data["MonthlyIncome"],
            data["OverTime"],
            int(prediction),
            float(probability)
        )

        cursor.execute(query, values)
        conn.commit()

        return {
            "prediction": int(prediction),
            "probability_of_leaving": float(probability)
        }

    except Exception as e:
        return {"error": str(e)}