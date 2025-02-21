import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_get_all_data():
    response = client.get("/all_data")
    assert response.status_code == 200
    assert isinstance(response.json(), list) or "error" in response.json()

@pytest.mark.parametrize("income, credit_score, debt_ratio, age, employment_years, expected_status", [
    (50000, 700, 0.3, 30, 5, 200),  # Geçerli veri
    (None, 700, 0.3, 30, 5, 422),  # Eksik gelir (income)
    (50000, None, 0.3, 30, 5, 422),  # Eksik kredi skoru
])
def test_predict(income, credit_score, debt_ratio, age, employment_years, expected_status):
    response = client.post("/predict", params={
        "income": income,
        "credit_score": credit_score,
        "debt_ratio": debt_ratio,
        "age": age,
        "employment_years": employment_years
    })
    assert response.status_code == expected_status

    if response.status_code == 200:
        assert "approved" in response.json()
        assert response.json()["approved"] in [0, 1]
    else:
        assert "error" in response.json()
