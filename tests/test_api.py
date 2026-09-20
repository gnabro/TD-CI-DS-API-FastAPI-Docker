from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# Test 1 : prédiction correcte avec [1.0, 2.0, 3.0]
def test_predict_correct():
    payload = {"features": [1.0, 2.0, 3.0]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert data["predictions"] == [2.0, 4.0, 6.0]


# Test 2 : prédiction incorrecte — on vérifie que la prédiction
# n'est PAS égale à une valeur volontairement fausse
def test_predict_incorrect():
    payload = {"features": [1.0, 2.0, 3.0]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Valeur attendue volontairement fausse
    valeur_fausse = [9999.0, 9999.0, 9999.0]
    # On vérifie que l'API ne renvoie PAS cette valeur fausse
    assert data["predictions"] != valeur_fausse


# Test 3 : JSON incorrect (features manquant)
def test_predict_invalid_json():
    payload = {"data": [3.5, 1.2, 4.9]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422