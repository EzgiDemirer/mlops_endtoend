import logging
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split
import uvicorn
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

file_path = "credit_approval_data.csv"
model_path = "xgboost_credit_model.pkl"


if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    logger.info("Dataset loaded successfully.")
else:
    df = pd.DataFrame()  
    logger.warning(f"Warning: {file_path} not found")

def train_xgboost():
    if df.empty:
        logger.error("Error: No data available for training!")
        return None

    try:
        features = ["income", "credit_score", "debt_ratio", "age", "employment_years"]
        X = df[features]
        y = df["approved"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
        model.fit(X_train, y_train)

        joblib.dump(model, model_path)
        logger.info("Model trained and saved successfully.")

        return model
    except Exception as e:
        logger.error(f"Model training failed: {e}")
        return None

# Model yükleme
if os.path.exists(model_path):
    model = joblib.load(model_path)
    logger.info("Model loaded successfully.")
else:
    logger.warning("Model not found, training a new one...")
    model = train_xgboost()

@app.get("/all_data")
async def get_all_data():
    if df.empty:
        return {"error": "No data available"}
    return df.to_dict(orient="records")

@app.post("/predict")
async def predict(income: float, credit_score: int, debt_ratio: float, age: int, employment_years: int):
    if model is None:
        logger.error("Prediction error: Model is missing!")
        return JSONResponse(status_code=500, content={"error": "Model not found or not trained"})

    input_data = pd.DataFrame([[income, credit_score, debt_ratio, age, employment_years]],
                              columns=["income", "credit_score", "debt_ratio", "age", "employment_years"])
    
    prediction = model.predict(input_data)[0]
    return {"approved": int(prediction)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
