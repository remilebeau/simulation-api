from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


# @desc test for triangular distribution
# @route GET /api/distributions/triangular
def test_distributions_triangular():
    params = {"distMin": 200, "distMode": 400, "distMax": 600}
    response = client.get(
        "/api/distributions/triangular",
        params=params,
    )
    response_two = client.get(
        "/api/distributions/triangular",
        params=params,
    )
    # check status code
    assert response.status_code == 200
    # check that 1000 values were returned
    assert len(response.json()["distValues"]) == 1000
    # check that the 1000 values are reproducible with the same inputs
    assert response.json()["distValues"] == response_two.json()["distValues"]
    # check that the 1000 values are not identical
    assert min(response.json()["distValues"]) < max(response.json()["distValues"])


# @desc test for uniform distribution
# @route GET /api/distributions/uniform
def test_distributions_uniform():
    params = {"distMin": 200, "distMax": 600}
    response = client.get(
        "/api/distributions/uniform",
        params=params,
    )
    response_two = client.get(
        "/api/distributions/uniform",
        params=params,
    )
    # check status code
    assert response.status_code == 200
    # check that 1000 values were returned
    assert len(response.json()["distValues"]) == 1000
    # check that the 1000 values are reproducible with the same inputs
    assert response.json()["distValues"] == response_two.json()["distValues"]
    # check that the 1000 values are not identical
    assert min(response.json()["distValues"]) < max(response.json()["distValues"])


# @desc test for normal distribution
# @route GET /api/distributions/normal
def test_distributions_normal():
    params = {
        "distMin": 200,
        "distMean": 400,
        "distMax": 600,
        "distSD": 100,
    }
    response = client.get(
        "/api/distributions/normal",
        params=params,
    )
    response_two = client.get(
        "/api/distributions/normal",
        params=params,
    )
    # check status code
    assert response.status_code == 200
    # check that 1000 values were returned
    assert len(response.json()["distValues"]) == 1000
    # check that the 1000 values are reproducible with the same inputs
    assert response.json()["distValues"] == response_two.json()["distValues"]
    # check that the 1000 values are not identical
    assert min(response.json()["distValues"]) < max(response.json()["distValues"])


# @desc test for truncated normal distribution
# @route GET /api/distributions/truncated_normal
def test_distributions_truncated_normal():
    params = {
        "distMin": 200,
        "distMean": 400,
        "distMax": 600,
        "distSD": 100,
    }
    response = client.get(
        "/api/distributions/truncated_normal",
        params=params,
    )
    response_two = client.get(
        "/api/distributions/truncated_normal",
        params=params,
    )
    # check status code
    assert response.status_code == 200
    # check that 1000 values were returned
    assert len(response.json()["distValues"]) == 1000
    # check that the 1000 values are reproducible with the same inputs
    assert response.json()["distValues"] == response_two.json()["distValues"]
    # check that the 1000 values are not identical
    assert min(response.json()["distValues"]) < max(response.json()["distValues"])
