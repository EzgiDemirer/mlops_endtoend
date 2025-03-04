import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.parametrize("income, credit_score, debt_ratio, age, employment_years, expected_status", [
    (50000, 700, 0.3, 30, 5, 200),  
    (None, 700, 0.3, 30, 5, 422),  
    (50000, None, 0.3, 30, 5, 422),  
])
def test_predict(income, credit_score, debt_ratio, age, employment_years, expected_status):
    params = {
        "income": income,
        "credit_score": credit_score,
        "debt_ratio": debt_ratio,
        "age": age,
        "employment_years": employment_years
    }

    params = {k: v for k, v in params.items() if v is not None}

    response = client.post("/predict", params=params)
    assert response.status_code == expected_status

    if response.status_code == 200:
        assert "approved" in response.json()
        assert response.json()["approved"] in [0, 1]
    else:
      
        error_response = response.json()
        assert "detail" in error_response  
        assert isinstance(error_response["detail"], list)  
