# tests/test_api.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_predict_success():
    """1) Valide une prédiction correcte avec [1.0, 2.0, 3.0]"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.post("/predict", json={"features": [1.0, 2.0, 3.0]})
    assert resp.status_code == 200
    assert resp.json() == {"predictions": [2.0, 4.0, 6.0]}

@pytest.mark.anyio
async def test_predict_incorrect_expected():
    """2) Valide une prédiction avec un résultat attendu volontairement faux (utilisation de !=)"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.post("/predict", json={"features": [1.0, 2.0, 3.0]})
    assert resp.status_code == 200
    # On vérifie que la réponse RÉELLE n'est PAS égale au résultat faux
    assert resp.json() != {"predictions": [99.0, 99.0, 99.0]}

@pytest.mark.anyio
async def test_predict_invalid_json():
    """3) Valide l'envoi d'un JSON incorrect (champ features manquant)"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.post("/predict", json={"feature1": 3.5, "feature2": 1.2, "feature3": 4.9})
    assert resp.status_code == 422