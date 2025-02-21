import pandas as pd
import pytest

# CSV dosyasını oku
file_path = "credit_approval_data.csv"
df = pd.read_csv(file_path)

def test_dataframe_not_empty():
    """Veri çerçevesinin boş olmadığını kontrol et"""
    assert not df.empty, "Veri kümesi boş!"

def test_columns_exist():
    """Tüm gerekli sütunların var olup olmadığını kontrol et"""
    required_columns = {"income", "credit_score", "debt_ratio", "age", "employment_years", "approved"}
    assert required_columns.issubset(df.columns), "Bazı sütunlar eksik!"

def test_no_negative_values():
    """Gelir, yaş ve çalışma yıllarının negatif olmamasını kontrol et"""
    assert (df["income"] >= 0).all(), "Gelir negatif!"
    assert (df["age"] >= 0).all(), "Yaş negatif!"
    assert (df["employment_years"] >= 0).all(), "Çalışma yılı negatif!"

def test_credit_score_range():
    """Kredi skorunun 300-850 arasında olup olmadığını kontrol et"""
    assert ((df["credit_score"] >= 300) & (df["credit_score"] <= 850)).all(), "Geçersiz kredi skoru!"

def test_approved_values():
    """Onay sütununun sadece 0 ve 1 değerlerinden oluştuğunu kontrol et"""
    assert df["approved"].isin([0, 1]).all(), "Onay sütunu 0 veya 1 olmalı!"