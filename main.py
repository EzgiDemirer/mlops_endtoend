from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
import uvicorn  # <== Uvicorn ekledik

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

file_path = "credit_approval_data.csv"

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    df = pd.DataFrame()  # Eğer dosya yoksa boş bir DataFrame kullan

def train_xgboost():
    if df.empty:
        return "Data file not found. Model training skipped."

    features = ["income", "credit_score", "debt_ratio", "age", "employment_years"]
    X = df[features]
    y = df["approved"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, "xgboost_credit_model.pkl")

try:
    model = joblib.load("xgboost_credit_model.pkl")
except:
    train_xgboost()
    try:
        model = joblib.load("xgboost_credit_model.pkl")
    except FileNotFoundError:
        model = None

@app.get("/all_data")
async def get_all_data():
    if df.empty:
        return {"error": "No data available"}
    return df.to_dict(orient="records")

@app.post("/predict")
async def predict(income: float, credit_score: int, debt_ratio: float, age: int, employment_years: int):
    if model is None:
        return {"error": "Model not found or not trained"}

    input_data = pd.DataFrame([[income, credit_score, debt_ratio, age, employment_years]],
                              columns=["income", "credit_score", "debt_ratio", "age", "employment_years"])
    
    prediction = model.predict(input_data)[0]

    return {"approved": int(prediction)}

# Eğer uygulama direkt çalıştırılıyorsa, 8080 portunda başlat
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
