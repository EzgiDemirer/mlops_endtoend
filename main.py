from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

file_path = "credit_approval_data.csv"
df = pd.read_csv(file_path)

def train_xgboost():
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
    model = joblib.load("xgboost_credit_model.pkl")

@app.get("/all_data")
async def get_all_data():
    return df.to_dict(orient="records")

@app.post("/predict")
async def predict(income: float, credit_score: int, debt_ratio: float, age: int, employment_years: int):
    input_data = pd.DataFrame([[income, credit_score, debt_ratio, age, employment_years]],
                              columns=["income", "credit_score", "debt_ratio", "age", "employment_years"])
    
    prediction = model.predict(input_data)[0]

    return {"approved": int(prediction)}
